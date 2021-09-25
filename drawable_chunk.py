from drawable import Drawable
from point2d import Point2d


class DrawableChunk(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.number = 0
        self.surface = None
        Point2d.size = Point2d(0, 0)
