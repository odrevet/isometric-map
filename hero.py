import pygame
import math

TILE_SIZE = 8


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("res/ryle.png")
        self.x = 0
        self.y = 16
        self.z = 16
        self.jump = False

    def get_index(self):
        return [
            math.ceil(self.x / (TILE_SIZE * 4)),
            math.ceil(self.y / (TILE_SIZE * 4)),
            math.ceil(self.z / (TILE_SIZE * 4)),
        ]
