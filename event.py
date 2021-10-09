from point3d import Point3d
from cube import Cube

class Event:
    size = Point3d(Cube.SIZE, Cube.SIZE, Cube.SIZE)
    def __init(self):
        self.position = Point3d(0, 0, 0)


class EventWarp(Event):
    def __init__(self):
        self.destination = None
