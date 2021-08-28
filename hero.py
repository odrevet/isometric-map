import pygame

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('res/ryle.png')
        self.x = 0
        self.y = 0
        self.z = 0
        self.jump = False
