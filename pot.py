import pygame

from drawable import Drawable
from point3d import Point3d
from cube import Cube

class Pot(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.image = pygame.image.load("res/pot.png")
        self.size = Point3d(Cube.SIZE, Cube.SIZE, Cube.SIZE)

    def draw(self, x, y, surface_display):
        surface_display.blit(self.image, (x, y))
