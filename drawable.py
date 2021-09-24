from point3d import Point3d

class Drawable():
    def __init__(self, x = 0, y = 0, z = 0):
        self.position = Point3d(x, y, z)
        self.zindex = 0
        self.is_top = None # temporary used to draw split sprite, to be removed