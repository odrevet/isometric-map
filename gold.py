import pygame

from drawable import Drawable
from point3d import Point3d
from cube import Cube


class Gold(Drawable):
    image = pygame.image.load("res/gold.png")

    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.size = Point3d(Cube.SIZE, Cube.SIZE, Cube.SIZE)
        self.solid = False
        self.amount = 5

    def draw(self, x, y, surface_display):
        surface_display.blit(self.image, (x, y))
