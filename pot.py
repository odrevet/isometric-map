import pygame

from drawable import Drawable


class Pot(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.image = pygame.image.load("res/pot.png")

    def draw(self, x, y, surface_display):
        surface_display.blit(self.image, (x, y))
