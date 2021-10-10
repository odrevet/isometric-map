import pygame

from drawable import Drawable
from pygame.math import Vector3
from cube import Cube


class NPC(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)

    def draw(self, x, y, surface_display):
        pass

class Woman(NPC):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.size = Vector3(Cube.SIZE, Cube.SIZE, Cube.SIZE * 2)
        self.image = pygame.image.load("res/NPC/woman/1_0.png")

    def draw(self, x, y, surface_display):
        surface_display.blit(self.image, (x, y))