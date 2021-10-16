import argparse

import pygame
from pygame.locals import *

import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox

from hero import Hero
from level import *
from cube import Cube
from pygame.math import Vector3
from game import Game

from levels.lv import *

parser = argparse.ArgumentParser()
parser.add_argument("--music", default=True, action=argparse.BooleanOptionalAction)
args = vars(parser.parse_args())

# init pygame
pygame.init()

resolution_screen = (320, 240)
resolution_window = (640, 480)
surface_window = pygame.display.set_mode(resolution_window)
surface_screen = pygame.Surface(resolution_screen)
pygame.display.set_caption("Isometric map")
camera = Vector2(0, 0)

game = Game()

# init GUI
game.ui_manager = pygame_gui.UIManager(
    resolution_screen, "data/themes/classic.json"
)
game.debug_textbox = UITextBox(
    "",
    pygame.Rect((0, 0), (320, 35)),
    manager=game.ui_manager,
    object_id="#debug_textbox",
)

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
level_1(game, surface_window, surface_screen)

while True:
    game.update()
    camera = cartesian_to_isometric((hero.position.x, hero.position.y))
    camera.x = resolution_screen[0] // 2 - camera.x
    camera.y = resolution_screen[1] // 2 - camera.y + hero.position.z
    game.draw(camera, surface_screen)

    scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
    surface_window.blit(scaled_win, (0, 0))
    pygame.display.update()
