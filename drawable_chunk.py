from drawable import Drawable
from point2d import Point2d


class DrawableChunk(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.number = 0
        self.surface = None
        Point2d.size = Point2d(0, 0)

    def draw(self, x, y, surface_display):
        z_shift = (self.size.y // 2) * self.number
        surface_display.blit(
            self.surface,
            (
                x,
                y + z_shift,
            ),
            (0, z_shift, self.size.x, self.size.y // 2),
        )
