from pygame.math import Vector3
from cube import Cube

class Event:
    size = Vector3(Cube.SIZE, Cube.SIZE, Cube.SIZE)
    def __init(self):
        self.position = Vector3(0, 0, 0)


class EventWarp(Event):
    def __init__(self):
        self.destination = None
