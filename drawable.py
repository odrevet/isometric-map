from abc import ABC

from point3d import Point3d
from const import CUBE_SIZE


class Drawable(ABC):
    def __init__(self, x=0, y=0, z=0):
        self.position = Point3d(x, y, z)
        self.zindex = 0
        self.update_zindex()
        self.size = Point3d(0,0,0)

    def update_zindex(self):
        self.zindex = sum(
            list(map((lambda position: position // CUBE_SIZE), self.position.list()))
        )

    def intersect(self, other):
        return (
            self.position.y + self.size.y > other.position.y
            and self.position.y < other.position.y + other.size.y
            and self.position.x + self.size.x > other.position.x
            and self.position.x < other.position.x + other.size.x
        )

    def draw(self, x, y, surface_display):
        pass

    def __str__(self):
        return f"{type(self).__name__} at {self.position} zindex {self.zindex}"
