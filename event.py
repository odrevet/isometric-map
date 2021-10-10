from pygame.math import Vector3
from cube import Cube

class Event:
    size = Vector3(Cube.SIZE, Cube.SIZE, Cube.SIZE)

    def __init__(self, x, y, z):
        self.position = Vector3(x, y, z)
        self.on_intersect = None

class EventWarp(Event):
    def __init__(self):
        self.destination = None
