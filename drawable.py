from abc import ABC

from pygame.math import Vector3
from const import CUBE_SIZE


class Drawable(ABC):
    def __init__(self, x=0, y=0, z=0):
        self.position = Vector3(x, y, z)
        self.size = Vector3(0, 0, 0)
        self.zindex = 0
        self.update_zindex()
        self.solid = True
        self.draggable = False

    def update_zindex(self):
        self.zindex = sum(
            self.position // CUBE_SIZE
        )

    def intersect(self, other):
        return (
            self.position.y + self.size.y > other.position.y
            and self.position.y < other.position.y + other.size.y
            and self.position.x + self.size.x > other.position.x
            and self.position.x < other.position.x + other.size.x
            and self.position.z + self.size.z > other.position.z
            and self.position.z < other.position.z + other.size.z
        )

    def intersect_Vector3(self, Vector3):
        return (
            self.position.y + self.size.y >= Vector3.y
            and self.position.y <= Vector3.y
            and self.position.x + self.size.x >= Vector3.x
            and self.position.x <= Vector3.x
            and self.position.z + self.size.z >= Vector3.z
            and self.position.z <= Vector3.z
        )

    def get_coords(self):
        bl = Vector3(self.position.x, self.position.y + self.size.y, self.position.z)
        br = Vector3(
            self.position.x + self.size.x,
            self.position.y + self.size.y,
            self.position.z,
        )
        tl = Vector3(self.position.x, self.position.y, self.position.z)
        tr = Vector3(self.position.x + self.size.x, self.position.y, self.position.z)
        return (bl, br, tl, tr)

    def draw(self, x, y, surface_display):
        pass

    def __str__(self):
        return f"{type(self).__name__} \t pos {self.position} \t size {self.size} \t zindex {int(self.zindex)}"
