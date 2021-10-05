import pygame
from cube import Cube

from drawable import Drawable
from point3d import Point3d


class Chest(Drawable):
    image = pygame.image.load("res/chest.png")

    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.size = Point3d(Cube.SIZE - 1, Cube.SIZE - 1, Cube.SIZE - 1)

    def draw(self, x, y, surface_display):
        surface_display.blit(self.image, (x, y))
