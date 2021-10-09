import pygame
from pygame.math import Vector3

from cube import Cube

from drawable import Drawable


class Chest(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.size = Vector3(Cube.SIZE - 1, Cube.SIZE - 1, Cube.SIZE - 1)
        self.is_open = False
        self.content = None
        self.on_open = None
        self.id = None

        self.closed = pygame.image.load("res/chest/chest_0.png").convert_alpha()
        self.half_full = pygame.image.load("res/chest/chest_1.png").convert_alpha()
        self.open_full = pygame.image.load("res/chest/chest_2.png").convert_alpha()
        self.open_empty = pygame.image.load("res/chest/chest_3.png").convert_alpha()
        self.half_empty = pygame.image.load("res/chest/chest_4.png").convert_alpha()

    def draw(self, x, y, surface_display):
        surface = None
        if self.is_open:
            surface = self.open_full
        else:
            surface = self.closed

        surface_display.blit(surface, (x, y - (surface.get_height() - Cube.SIZE * 2)))

    def open(self):
        self.is_open = True
        self.on_open()