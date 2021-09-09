import pygame
import math

TILE_SIZE = 8


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("res/ryle.png")
        self.x = 0
        self.y = 0
        self.z = 16
        self.jump = False
        self.depth = 32
        self.size = 16

    def get_coords(self):
            bl = self.x, self.y + self.size
            br = self.x + self.size , self.y + self.size
            tl = self.x, self.y
            tr = self.x + self.size, self.y
            return (bl, br, tl, tr)

    def get_index(self):
        return [
            math.ceil(self.x / (TILE_SIZE * 4)),
            math.ceil(self.y / (TILE_SIZE * 4)),
            math.ceil(self.z / (TILE_SIZE * 4)),
        ]
