import pygame
from vector import Vector
from utils import draw_vector
from typing import Union
from config import *
import random
from config import return_colors
import dearpygui.dearpygui as dpg


class Particle:
    def __init__(self, pos: Vector, vel: Vector, mass: float, radius: float):
        self.pos = pos
        self.vel = vel
        self.acc = Vector(0.0, 0.0)
        self.mass = float(mass)
        self.radius = float(radius)
        self.color = random.choice(return_colors())
        self.trail = []
        self.trail_length = return_trail_length()

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.acc = Vector(0, 0)
        self.trail.append(self.pos.as_tuple())
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw(self, screen, show_vectors: bool = False):
        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail))) if TRAIL_FADE else 255
                trail_color = (*self.color[:3], alpha)
                pygame.draw.line(
                    screen, trail_color, self.trail[i], self.trail[i + 1], 2
                )

        pygame.draw.circle(screen, self.color, self.pos.as_tuple(), int(self.radius))

        if show_vectors:
            try:
                base_scale = dpg.get_value("vector_scale")
            except:
                base_scale = 1.0

            scale_factor = base_scale * max(0.1, self.radius / 20.0)

            if self.vel.magnitude() > 0:
                draw_vector(screen, self.pos, self.vel, (255, 0, 0), 0.1 * scale_factor)

            if self.acc.magnitude() > 0:
                draw_vector(screen, self.pos, self.acc, (0, 255, 0), 0.2 * scale_factor)
