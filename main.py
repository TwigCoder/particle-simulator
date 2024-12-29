import pygame
import dearpygui.dearpygui as dpg
from simulator import PhysicsSimulator
from gui import GUI
from config import *
import sys


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Physics Simulator")

    dpg.create_context()
    dpg.create_viewport(title="Physics Simulator Controls", width=400, height=600)
    dpg.setup_dearpygui()

    simulator = PhysicsSimulator(screen)
    gui = GUI(simulator)

    dpg.show_viewport()

    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            gui.handle_mouse_events(event)

        simulator.update(dt)

        gui.update_stats()

        screen.fill(BACKGROUND_COLOR)
        simulator.draw()
        pygame.display.flip()

        dpg.render_dearpygui_frame()

    dpg.destroy_context()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
