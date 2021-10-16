import pygame
from pygame.math import Vector3
import pyganim

from drawable import Drawable
from cube import Cube
from direction import Direction

class NPC(Drawable):
    def __init__(self, type, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.type = type
        self.size = Vector3(Cube.SIZE, Cube.SIZE, Cube.SIZE * 2)
        self.image = pygame.image.load(f"res/NPC/{self.type}/walk_down_0.png")
        self.on_interact = None

        anim_types = ["walk_up", "walk_down"]
        self.anim_objs = {}
        for anim_type in anim_types:
            images_with_duration = [
                ((f"res/NPC/{self.type}/{anim_type}_{str(num)}.png"), 100) for num in range(4)
            ]
            self.anim_objs[anim_type] = pyganim.PygAnimation(images_with_duration)

        self.anim_objs["walk_right"] = self.anim_objs["walk_down"].getCopy()
        self.anim_objs["walk_right"].flip(True, False)
        self.anim_objs["walk_right"].makeTransformsPermanent()
        self.anim_objs["walk_left"] = self.anim_objs["walk_up"].getCopy()
        self.anim_objs["walk_left"].flip(True, False)
        self.anim_objs["walk_left"].makeTransformsPermanent()


    def draw(self, x, y, surface_display):
        surface_display.blit(self.image, (x, y - 16))
