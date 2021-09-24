from drawable import Drawable


class DrawableChunk(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.number = 0
