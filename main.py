import argparse

import pygame
from pygame.locals import *

from hero import Hero
from level import *
from cube import Cube
from game import Game

from levels.lv import *

parser = argparse.ArgumentParser()
parser.add_argument("--music", default=True, action=argparse.BooleanOptionalAction)
args = vars(parser.parse_args())

# init pygame
pygame.init()
pygame.display.set_caption("Isometric map")

game = Game()

# Music
if args["music"]:
    try:
        pygame.mixer.music.load("res/music/overworld_2.mid")
        pygame.mixer.music.play()
    except:
        print("Midi device not found")
        pass

# init hero
hero = Hero(z=Cube.SIZE)
game.hero = hero

# init level
game.level = Level()
level_1(game)

while True:
    game.update()
    game.draw()
    game.update_display()
