import pygame
from pygame.locals import *

import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox

from hero import Hero
from pot import Pot
from chest import Chest
from gold import Gold
from level import *
from cube import Cube
from point2d import Point2d
from game import Game


# init pygame
pygame.init()

resolution_screen = Point2d(320, 240)
resolution_window = Point2d(640, 480)
surface_window = pygame.display.set_mode(resolution_window.list())
surface_screen = pygame.Surface(resolution_screen.list())
pygame.display.set_caption("Isometric map")
camera = Point2d(resolution_screen.x // 2, resolution_screen.y // 2)

game = Game()

# init GUI
game.ui_manager = pygame_gui.UIManager(
    resolution_screen.list(), "data/themes/classic.json"
)
game.debug_textbox = UITextBox(
    "",
    pygame.Rect((0, 0), (320, 35)),
    manager=game.ui_manager,
    object_id="#debug_textbox",
)

# Music
#try:
#    pygame.mixer.music.load("res/music/overworld_2.mid")
#    pygame.mixer.music.play()
#except:
#    pass

# init level
game.level = Level()
game.level.read("data/level.map")

# init hero
hero = Hero(z=Cube.SIZE)
game.hero = hero 

# create drawables
pot = Pot(Cube.SIZE, Cube.SIZE, Cube.SIZE * 4)
chest = Chest(Cube.SIZE * 2, 0, Cube.SIZE)
gold = Gold(Cube.SIZE * 2, Cube.SIZE * 2, Cube.SIZE)

# add drawables
game.add_drawable(pot)
game.add_drawable(chest)
game.add_drawable(gold)
game.add_drawable(hero)

while True:
    game.update()
    game.draw(camera, surface_screen)

    scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
    surface_window.blit(scaled_win, (0, 0))
    pygame.display.update()
