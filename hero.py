from enum import Enum
import math

import pygame
import pyganim

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

        self.image_up = pygame.image.load("res/ryle/up.png")
        self.image_down = pygame.image.load("res/ryle/down.png")
        self.image_left = pygame.transform.flip(self.image_up, True, False)
        self.image_right = pygame.transform.flip(self.image_down, True, False)

        anim_types = ["walk_up", "walk_down"]
        self.anim_objs = {}
        for anim_type in anim_types:
            images_with_duration = [
                ((f"res/ryle/{anim_type}_{str(num)}.png"), 100) for num in range(8)
            ]
            self.anim_objs[anim_type] = pyganim.PygAnimation(images_with_duration)

        self.anim_objs["walk_right"] = self.anim_objs["walk_down"].getCopy()
        self.anim_objs["walk_right"].flip(True, False)
        self.anim_objs["walk_right"].makeTransformsPermanent()
        self.anim_objs["walk_left"] = self.anim_objs["walk_up"].getCopy()
        self.anim_objs["walk_left"].flip(True, False)
        self.anim_objs["walk_left"].makeTransformsPermanent()

        self.moveConductor = pyganim.PygConductor(self.anim_objs)

        self.x = 0
        self.y = 0
        self.z = CUBE_SIZE
        self.jump = False
        self.jump_max = CUBE_SIZE * 1.5
        self.jump_cur = 0
        self.depth = CUBE_SIZE * 2
        self.size = CUBE_SIZE - 1
        

    def get_coords(self):
        bl = [self.x, self.y + self.size]
        br = [self.x + self.size, self.y + self.size]
        tl = [self.x, self.y]
        tr = [self.x + self.size, self.y]
        return (bl, br, tl, tr)

    def get_index(self):
        return [
            math.ceil(self.x / (TILE_SIZE * 4)),
            math.ceil(self.y / (TILE_SIZE * 4)),
            math.ceil(self.z / (TILE_SIZE * 4)),
        ]

    def draw(self, x, y, surface_display):
        self.moveConductor.play()

        if self.direction == Direction.UP:
            self.anim_objs["walk_up"].blit(surface_display, (x, y))
        elif self.direction == Direction.RIGHT:
            self.anim_objs["walk_right"].blit(surface_display, (x, y))
        elif self.direction == Direction.DOWN:
            self.anim_objs["walk_down"].blit(surface_display, (x, y))
        elif self.direction == Direction.LEFT:
            self.anim_objs["walk_left"].blit(surface_display, (x, y))
