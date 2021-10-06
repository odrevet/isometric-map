class Point3d:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def list(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        return f"{self.x}:{self.y}:{self.z}"
