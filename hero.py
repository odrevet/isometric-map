import pygame
import math

from const import *


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("res/down.png")
        self.x = 0
        self.y = 0
        self.z = CUBE_SIZE
        self.jump = False
        self.depth = CUBE_SIZE * 2
        self.size = CUBE_SIZE

    def get_coords(self):
        bl = self.x, self.y + self.size
        br = self.x + self.size, self.y + self.size
        tl = self.x, self.y
        tr = self.x + self.size, self.y
        return (bl, br, tl, tr)

    def get_index(self):
        return [
            math.ceil(self.x / (TILE_SIZE * 4)),
            math.ceil(self.y / (TILE_SIZE * 4)),
            math.ceil(self.z / (TILE_SIZE * 4)),
        ]
