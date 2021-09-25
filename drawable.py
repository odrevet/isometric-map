from abc import ABC

from pygame.display import update
from point3d import Point3d


class Drawable(ABC):
    def __init__(self, x=0, y=0, z=0):
        self.position = Point3d(x, y, z)
        self.zindex = 0
        self.update_zindex()

    def update_zindex(self):
        cube_size = 16  # TODO get from Cube
        self.zindex = sum(list(map((lambda x: x // cube_size), self.position.list())))

    def draw(self, x, y, surface_display):
        pass
