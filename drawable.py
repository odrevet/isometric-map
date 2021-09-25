from abc import ABC
from point3d import Point3d


class Drawable(ABC):
    def __init__(self, x=0, y=0, z=0):
        self.position = Point3d(x, y, z)
        self.zindex = 0

    def draw(self, x, y, surface_display):
        pass
