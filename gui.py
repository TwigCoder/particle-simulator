import dearpygui.dearpygui as dpg
from particle import Particle
from vector import Vector
import random
from config import *
import pygame
from simulator import ForceField, ParticleEmitter


class GUI:
    def __init__(self, simulator):
        self.simulator = simulator
        self.setup_gui()
        self.creating_field = False
        self.creating_emitter = False

    def setup_gui(self):
        with dpg.window(label="Controls", pos=(0, 0)):
            with dpg.group():
                dpg.add_checkbox(
                    label="Enable Gravity",
                    default_value=True,
                    callback=self.toggle_gravity,
                )
                dpg.add_checkbox(
                    label="Enable Collisions",
                    default_value=True,
                    callback=self.toggle_collisions,
                )

                dpg.add_separator()
                dpg.add_text("Vector Display")
                dpg.add_checkbox(
                    label="Show Vectors",
                    default_value=False,
                    callback=self.toggle_vectors,
                )
                dpg.add_slider_float(
                    label="Vector Scale",
                    default_value=1.0,
                    min_value=0.1,
                    max_value=5.0,
                    callback=self.update_vector_scale,
                    tag="vector_scale",
                )

                dpg.add_separator()

                dpg.add_button(
                    label="Add Random Particle", callback=self.add_random_particle
                )
                dpg.add_button(
                    label="Clear All Particles", callback=self.clear_particles
                )

                dpg.add_separator()
                dpg.add_text("Particle Properties")

                dpg.add_slider_float(
                    label="Mass",
                    default_value=2.0,
                    min_value=0.5,
                    max_value=10.0,
                    tag="mass_slider",
                )

                dpg.add_slider_float(
                    label="Initial Velocity",
                    default_value=100.0,
                    min_value=0.0,
                    max_value=300.0,
                    tag="velocity_slider",
                )

                dpg.add_slider_float(
                    label="Direction (degrees)",
                    default_value=0.0,
                    min_value=0.0,
                    max_value=360.0,
                    tag="direction_slider",
                )

                dpg.add_button(
                    label="Add Particle (or Click in Simulation)",
                    callback=self.add_particle_at_center,
                )

        with dpg.window(label="Particle Emitters", pos=(0, 800), width=380, height=250):
            with dpg.group():
                dpg.add_text("Emitter Controls", color=(255, 255, 0))
                dpg.add_separator()

                dpg.add_slider_float(
                    label="Emission Rate (particles/s)",
                    default_value=2.0,
                    min_value=0.1,
                    max_value=10.0,
                    tag="emitter_rate",
                )

                dpg.add_slider_float(
                    label="Min Speed",
                    default_value=30.0,
                    min_value=10.0,
                    max_value=100.0,
                    tag="min_speed",
                )

                dpg.add_slider_float(
                    label="Max Speed",
                    default_value=80.0,
                    min_value=10.0,
                    max_value=150.0,
                    tag="max_speed",
                )

                dpg.add_slider_float(
                    label="Start Angle",
                    default_value=0.0,
                    min_value=0.0,
                    max_value=360.0,
                    tag="start_angle",
                )
                dpg.add_slider_float(
                    label="End Angle",
                    default_value=360.0,
                    min_value=0.0,
                    max_value=360.0,
                    tag="end_angle",
                )

                dpg.add_button(
                    label="Create Emitter (Middle Click)",
                    callback=self.toggle_emitter_creation_mode,
                )
                dpg.add_button(label="Clear All Emitters", callback=self.clear_emitters)

        with dpg.window(label="Statistics", pos=(0, 400), width=380, height=200):
            with dpg.group():
                dpg.add_text("System Statistics", color=(255, 255, 0))
                dpg.add_separator()

                dpg.add_text("Particle Count: 0", tag="particle_count")
                dpg.add_text("Average Velocity: 0 px/s", tag="avg_velocity")
                dpg.add_text("System Energy: 0 J", tag="system_energy")

                dpg.add_separator()

                dpg.add_text("Max Velocity: 0 px/s", tag="max_velocity")
                dpg.add_text("Total Mass: 0 kg", tag="total_mass")
                dpg.add_text("Average Mass: 0 kg", tag="avg_mass")

        with dpg.window(label="Force Fields", pos=(0, 600), width=380, height=200):
            with dpg.group():
                dpg.add_text("Force Field Controls", color=(255, 255, 0))
                dpg.add_separator()

                dpg.add_combo(
                    label="Field Type",
                    items=["ATTRACTOR", "REPULSOR"],
                    default_value="ATTRACTOR",
                    tag="field_type",
                )

                dpg.add_slider_float(
                    label="Field Strength",
                    default_value=500,
                    min_value=FORCE_FIELD_MIN_STRENGTH,
                    max_value=FORCE_FIELD_MAX_STRENGTH,
                    tag="field_strength",
                )

                dpg.add_slider_float(
                    label="Field Radius",
                    default_value=100,
                    min_value=FORCE_FIELD_MIN_RADIUS,
                    max_value=FORCE_FIELD_MAX_RADIUS,
                    tag="field_radius",
                )

                dpg.add_button(
                    label="Create Force Field (Right Click)",
                    callback=self.toggle_field_creation_mode,
                )
                dpg.add_button(
                    label="Clear All Fields", callback=self.clear_force_fields
                )

    def toggle_gravity(self, sender, app_data):
        self.simulator.gravity_enabled = app_data

    def toggle_collisions(self, sender, app_data):
        self.simulator.collision_enabled = app_data

    def toggle_vectors(self, sender, app_data):
        self.simulator.show_vectors = app_data

    def add_random_particle(self):
        pos = Vector(
            float(random.randint(50, WINDOW_WIDTH - 50)),
            float(random.randint(50, WINDOW_HEIGHT - 50)),
        )
        vel = Vector(random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0))
        mass = random.uniform(1.0, 5.0)
        radius = float(random.randint(10, 20))

        particle = Particle(pos, vel, mass, radius)
        self.simulator.add_particle(particle)

    def add_particle_at_center(self):
        center_pos = Vector(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        mass = dpg.get_value("mass_slider")
        velocity_magnitude = dpg.get_value("velocity_slider")
        direction_degrees = dpg.get_value("direction_slider")

        vel = Vector(1, 0).rotate(direction_degrees) * velocity_magnitude
        radius = mass * 5

        particle = Particle(center_pos, vel, mass, radius)
        self.simulator.add_particle(particle)

    def clear_particles(self):
        self.simulator.particles.clear()

    def update_vector_scale(self, sender, app_data):
        self.simulator.vector_scale = app_data

    def toggle_emitter_creation_mode(self):
        self.creating_emitter = not self.creating_emitter

    def clear_emitters(self):
        self.simulator.emitters.clear()

    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = Vector(*pygame.mouse.get_pos())

                mass = dpg.get_value("mass_slider")
                velocity_magnitude = dpg.get_value("velocity_slider")
                direction_degrees = dpg.get_value("direction_slider")

                vel = Vector(1, 0).rotate(direction_degrees) * velocity_magnitude
                radius = mass * 5

                particle = Particle(mouse_pos, vel, mass, radius)
                self.simulator.add_particle(particle)

            elif event.button == 2 and self.creating_emitter:
                mouse_pos = Vector(*pygame.mouse.get_pos())

                emitter = ParticleEmitter(
                    pos=mouse_pos,
                    rate=dpg.get_value("emitter_rate"),
                    velocity_range=(
                        dpg.get_value("min_speed"),
                        dpg.get_value("max_speed"),
                    ),
                    angle_range=(
                        dpg.get_value("start_angle"),
                        dpg.get_value("end_angle"),
                    ),
                    size_range=(3.0, 8.0),
                    max_particles=50,
                )
                self.simulator.add_emitter(emitter)

            elif event.button == 3 and self.creating_field:
                mouse_pos = Vector(*pygame.mouse.get_pos())
                field_type = dpg.get_value("field_type")
                strength = dpg.get_value("field_strength")
                radius = dpg.get_value("field_radius")

                field = ForceField(mouse_pos, strength, radius, field_type)
                self.simulator.force_fields.append(field)

    def toggle_field_creation_mode(self):
        self.creating_field = not self.creating_field

    def clear_force_fields(self):
        self.simulator.force_fields.clear()

    def update_stats(self):
        particles = self.simulator.particles
        count = len(particles)

        if count > 0:
            velocities = [p.vel.magnitude() for p in particles]
            masses = [p.mass for p in particles]

            avg_vel = sum(velocities) / count
            max_vel = max(velocities) if velocities else 0
            total_mass = sum(masses)
            avg_mass = total_mass / count

            energy = sum(0.5 * p.mass * p.vel.magnitude() ** 2 for p in particles)

            dpg.set_value("particle_count", f"Particle Count: {count}")
            dpg.set_value("avg_velocity", f"Average Velocity: {avg_vel:.1f} px/s")
            dpg.set_value("max_velocity", f"Max Velocity: {max_vel:.1f} px/s")
            dpg.set_value("system_energy", f"System Energy: {energy:.1f} J")
            dpg.set_value("total_mass", f"Total Mass: {total_mass:.1f} kg")
            dpg.set_value("avg_mass", f"Average Mass: {avg_mass:.1f} kg")
        else:
            dpg.set_value("particle_count", "Particle Count: 0")
            dpg.set_value("avg_velocity", "Average Velocity: 0 px/s")
            dpg.set_value("max_velocity", "Max Velocity: 0 px/s")
            dpg.set_value("system_energy", "System Energy: 0 J")
            dpg.set_value("total_mass", "Total Mass: 0 kg")
            dpg.set_value("avg_mass", "Average Mass: 0 kg")
