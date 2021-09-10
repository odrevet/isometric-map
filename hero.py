from enum import Enum
import math

import pygame

from const import *


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = Direction.DOWN
        
        self.image_up = pygame.image.load('res/up.png')
        self.image_down = pygame.image.load('res/down.png')
        self.image_left = pygame.transform.flip(self.image_up, True, False)
        self.image_right = pygame.transform.flip(self.image_down, True, False)

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

    def draw(self, x, y, surface_display):
        image = None
        if self.direction == Direction.UP:
            image = self.image_up
        elif self.direction == Direction.RIGHT:
            image = self.image_right
        elif self.direction == Direction.DOWN:
            image = self.image_down
        elif self.direction == Direction.LEFT:
            image = self.image_left
        
        surface_display.blit(
            image,
            (
                x,
                y,
            ),
        )
