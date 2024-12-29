import pygame
from particle import Particle
from vector import Vector
from config import *
import random
import math


class ForceField:
    def __init__(
        self, pos: Vector, strength: float, radius: float, field_type: str = "ATTRACTOR"
    ):
        self.pos = pos
        self.strength = strength
        self.radius = radius
        self.field_type = field_type
        self.color = FORCE_FIELD_COLORS[field_type]
        self.active = True

    def apply(self, particle: Particle):
        if not self.active:
            return

        diff = self.pos - particle.pos
        dist = diff.magnitude()

        if dist < self.radius:
            force_magnitude = self.strength * (1 - (dist / self.radius) ** 2)
            if self.field_type == "REPULSOR":
                force_magnitude *= -1

            force = diff.normalize() * force_magnitude
            particle.apply_force(force)

    def draw(self, screen):

        if not self.active:
            return

        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.color, (self.radius, self.radius), self.radius)
        screen.blit(surface, (self.pos.x - self.radius, self.pos.y - self.radius))

        pygame.draw.circle(screen, (255, 255, 255), self.pos.as_tuple(), 5)


class ParticleEmitter:
    def __init__(
        self,
        pos: Vector,
        rate: float,
        velocity_range: tuple[float, float],
        angle_range: tuple[float, float],
        size_range: tuple[float, float],
        max_particles: int = 50,
    ):
        self.pos = pos
        self.rate = max(0.1, rate)
        self.velocity_range = velocity_range
        self.angle_range = angle_range
        self.size_range = size_range
        self.max_particles = max_particles
        self.timer = 0
        self.active = True

    def update(self, dt, simulator):
        if not self.active:
            return

        if len(simulator.particles) < self.max_particles:
            self.timer += dt
            spawn_interval = 1.0 / self.rate

            if self.timer >= spawn_interval:
                self.spawn_particle(simulator)
                self.timer -= spawn_interval

    def spawn_particle(self, simulator):
        angle = random.uniform(self.angle_range[0], self.angle_range[1])
        speed = random.uniform(self.velocity_range[0], self.velocity_range[1])
        vel = Vector(1, 0).rotate(angle) * speed

        size = random.uniform(self.size_range[0], self.size_range[1])
        mass = size / 5.0

        particle = Particle(
            pos=Vector(self.pos.x, self.pos.y), vel=vel, mass=mass, radius=size
        )
        simulator.add_particle(particle)

    def draw(self, screen):
        if not self.active:
            return

        pygame.draw.circle(screen, (200, 200, 200), self.pos.as_tuple(), 10)

        pygame.draw.circle(screen, (100, 100, 100), self.pos.as_tuple(), 8)

        if abs(self.angle_range[1] - self.angle_range[0]) < 360:
            start_angle = math.radians(self.angle_range[0])
            end_angle = math.radians(self.angle_range[1])

            points = []
            center = self.pos.as_tuple()
            radius = 15

            points.append(center)

            for angle in range(
                int(self.angle_range[0]), int(self.angle_range[1]) + 1, 10
            ):
                rad = math.radians(angle)
                x = center[0] + radius * math.cos(rad)
                y = center[1] + radius * math.sin(rad)
                points.append((int(x), int(y)))

            if len(points) > 2:
                pygame.draw.polygon(screen, (150, 150, 150), points, 1)


class PhysicsSimulator:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.MAX_PARTICLES = 2000
        self.gravity_enabled = True
        self.collision_enabled = True
        self.show_vectors = False
        self.force_fields = []
        self.vector_scale = 1.0
        self.emitters = []

    def add_particle(self, particle):
        if len(self.particles) < self.MAX_PARTICLES:
            self.particles.append(particle)

    def remove_particle(self, particle):
        if particle in self.particles:
            self.particles.remove(particle)

    def set_vector_scale(self, scale):
        self.vector_scale = scale

    def add_emitter(self, emitter):
        self.emitters.append(emitter)

    def remove_emitter(self, emitter):
        if emitter in self.emitters:
            self.emitters.remove(emitter)

    def update(self, dt):
        for particle in self.particles:
            for emitter in self.emitters:
                emitter.update(dt, self)

            if self.gravity_enabled:
                particle.apply_force(Vector(0, GRAVITY * particle.mass))

            for field in self.force_fields:
                field.apply(particle)

            particle.update(dt)

            self.handle_boundary_collision(particle)

            if self.collision_enabled:
                for other in self.particles:
                    if particle != other:
                        self.check_collision(particle, other)

    def draw(self):
        for field in self.force_fields:
            field.draw(self.screen)

        for emitter in self.emitters:
            emitter.draw(self.screen)

        for particle in self.particles:
            particle.draw(self.screen, self.show_vectors)

    def handle_boundary_collision(self, particle):
        if particle.pos.y + particle.radius > WINDOW_HEIGHT:
            particle.pos.y = WINDOW_HEIGHT - particle.radius
            particle.vel.y *= -RESTITUTION

        if particle.pos.y - particle.radius < 0:
            particle.pos.y = particle.radius
            particle.vel.y *= -RESTITUTION

        if particle.pos.x + particle.radius > WINDOW_WIDTH:
            particle.pos.x = WINDOW_WIDTH - particle.radius
            particle.vel.x *= -RESTITUTION

        if particle.pos.x - particle.radius < 0:
            particle.pos.x = particle.radius
            particle.vel.x *= -RESTITUTION

    def check_collision(self, p1, p2):
        diff = p2.pos - p1.pos
        dist = diff.magnitude()

        if dist < p1.radius + p2.radius:
            normal = diff.normalize()
            relative_vel = p2.vel - p1.vel

            j = -(1 + RESTITUTION) * relative_vel.dot(normal)
            j /= 1 / p1.mass + 1 / p2.mass

            impulse = normal * j
            p1.vel -= impulse / p1.mass
            p2.vel += impulse / p2.mass

            overlap = (p1.radius + p2.radius - dist) / 2.0
            separation = normal * overlap

            p1.pos -= separation
            p2.pos += separation
