import math
from typing import Union


class Vector:
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: Union[int, float]):
        return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float]):
        return Vector(self.x / scalar, self.y / scalar)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return self / mag

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def rotate(self, angle: float):
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        x = self.x * cos_a - self.y * sin_a
        y = self.x * sin_a + self.y * cos_a
        return Vector(x, y)

    def as_tuple(self) -> tuple[int, int]:
        return (int(self.x), int(self.y))
