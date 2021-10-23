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
        self.on_interact = None
        self.direction = Direction.DOWN

        # animations
        anim_types = ["walk_up", "walk_down"]
        self.anim_objs = {}
        
        for anim_type in anim_types:
            images_with_duration = [
                ((f"res/NPC/{self.type}/{anim_type}_{str(num)}.png"), 130) for num in range(4)
            ]
            self.anim_objs[anim_type] = pyganim.PygAnimation(images_with_duration)

        self.anim_objs["walk_right"] = self.anim_objs["walk_down"].getCopy()
        self.anim_objs["walk_right"].flip(True, False)
        self.anim_objs["walk_right"].makeTransformsPermanent()
        self.anim_objs["walk_left"] = self.anim_objs["walk_up"].getCopy()
        self.anim_objs["walk_left"].flip(True, False)
        self.anim_objs["walk_left"].makeTransformsPermanent()

        self.moveConductor = pyganim.PygConductor(self.anim_objs)


    def draw(self, x, y, surface_display):
        animation_key = ""
        if self.direction == Direction.LEFT:
            animation_key = "walk_left"
        elif self.direction == Direction.UP:
            animation_key = "walk_up"
        elif self.direction == Direction.RIGHT:
            animation_key = "walk_right"
        elif self.direction == Direction.DOWN:
            animation_key = "walk_down"


        self.anim_objs[animation_key].currentFrameNum = 0
        self.anim_objs[animation_key].blit(surface_display, (x, y - 16))
