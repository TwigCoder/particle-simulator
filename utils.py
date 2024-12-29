import pygame
from vector import Vector
import math


def draw_vector(screen, start_pos, vector, color=(255, 0, 0), scale=1.0):
    if vector.magnitude() == 0:
        return

    line_width = 2
    arrow_size = 8

    end_pos = start_pos + vector * scale

    pygame.draw.line(
        screen, (*color, 200), start_pos.as_tuple(), end_pos.as_tuple(), line_width
    )

    if vector.magnitude() > 0:
        direction = vector.normalize()

        arrow_left = direction.rotate(135) * arrow_size
        arrow_right = direction.rotate(-135) * arrow_size

        arrow_point1 = end_pos + arrow_left
        arrow_point2 = end_pos + arrow_right

        pygame.draw.polygon(
            screen,
            (*color, 200),
            [end_pos.as_tuple(), arrow_point1.as_tuple(), arrow_point2.as_tuple()],
        )


def rotate_vector(vector, angle):
    x = vector.x * math.cos(math.radians(angle)) - vector.y * math.sin(
        math.radians(angle)
    )
    y = vector.x * math.sin(math.radians(angle)) + vector.y * math.cos(
        math.radians(angle)
    )
    return Vector(x, y)
