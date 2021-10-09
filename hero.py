import pygame
import pyganim

from enum import Enum
from drawable import Drawable
from const import *
from cube import Cube
from pygame.math import Vector3


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Hero(Drawable):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.direction = Direction.DOWN
        self.is_moving = False

        self.still_up = pygame.image.load("res/ryle/up.png").convert_alpha()
        self.still_down = pygame.image.load("res/ryle/down.png").convert_alpha()
        self.still_left = pygame.transform.flip(self.still_up, True, False)
        self.still_right = pygame.transform.flip(self.still_down, True, False)

        self.jump_up = pygame.image.load("res/ryle/jump_up_0.png").convert_alpha()
        self.jump_down = pygame.image.load("res/ryle/jump_down_0.png").convert_alpha()
        self.jump_left = pygame.transform.flip(self.jump_up, True, False)
        self.jump_right = pygame.transform.flip(self.jump_down, True, False)

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

        self.jump = False
        self.jump_max = Cube.SIZE * 1.5
        self.jump_cur = 0
        self.on_ground = None

        self.drawable_width = 32
        self.drawable_height = 48
        self.size = Vector3(Cube.SIZE - 1, Cube.SIZE - 1, 48)

        self.gold = 0
        self.life = 6

    def get_coords(self):
        bl = Vector3(self.position.x, self.position.y + self.size.y, self.position.z)
        br = Vector3(
            self.position.x + self.size.x,
            self.position.y + self.size.y,
            self.position.z,
        )
        tl = Vector3(self.position.x, self.position.y, self.position.z)
        tr = Vector3(self.position.x + self.size.x, self.position.y, self.position.z)
        return (bl, br, tl, tr)

    def draw(self, x, y, surface_display):
        if self.jump == True or self.on_ground == False:
            self.moveConductor.stop()
            if self.direction == Direction.UP:
                surface_display.blit(self.jump_up, (x, y))
            elif self.direction == Direction.RIGHT:
                surface_display.blit(self.jump_right, (x, y))
            elif self.direction == Direction.DOWN:
                surface_display.blit(self.jump_down, (x, y))
            elif self.direction == Direction.LEFT:
                surface_display.blit(self.jump_left, (x, y))
        elif self.is_moving == True:
            self.moveConductor.play()
            if self.direction == Direction.UP:
                self.anim_objs["walk_up"].blit(surface_display, (x, y))
            elif self.direction == Direction.RIGHT:
                self.anim_objs["walk_right"].blit(surface_display, (x, y))
            elif self.direction == Direction.DOWN:
                self.anim_objs["walk_down"].blit(surface_display, (x, y))
            elif self.direction == Direction.LEFT:
                self.anim_objs["walk_left"].blit(surface_display, (x, y))
        else:
            self.moveConductor.stop()
            if self.direction == Direction.UP:
                surface_display.blit(self.still_up, (x, y))
            elif self.direction == Direction.RIGHT:
                surface_display.blit(self.still_right, (x, y))
            elif self.direction == Direction.DOWN:
                surface_display.blit(self.still_down, (x, y))
            elif self.direction == Direction.LEFT:
                surface_display.blit(self.still_left, (x, y))
