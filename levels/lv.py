from functools import partial

import pygame

from event import Event
from pot import Pot
from chest import Chest
from gold import Gold
from cube import Cube
from NPC import *


def fade(game):
    fade = pygame.Surface((640, 480))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        game.surface_screen.blit(fade, (0, 0))
        game.update_display()


def warp(game, x, y, z):
    #fade(game)
    level_2(game)
    game.hero.position.x = x
    game.hero.position.y = y
    game.hero.position.z = z


def display_text(game, text):
    game.msg_textbox.show()
    game.msg_textbox.html_text = text
    game.msg_textbox.rebuild()
    loop = True

    while loop:
        time_delta = game.clock.tick(60) / 1000.0
        game.draw() 
        game.ui_manager.draw_ui(game.surface_screen)
        game.update_display()
        game.ui_manager.update(time_delta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_RETURN:
                    loop = False

    game.msg_textbox.hide()

def on_open_chest_1(game):
    game.hero.gold += 50
    display_text(game, "Found 50 Gold")

def level_1(game):
    game.level.clear()
    game.level.read("data/level.map")

    pot = Pot(Cube.SIZE * 6, Cube.SIZE * 5.5, Cube.SIZE)
    pot2 = Pot(Cube.SIZE * 6, Cube.SIZE * 3.5, Cube.SIZE)
    chest = Chest(Cube.SIZE * 2, Cube.SIZE * 6, Cube.SIZE)
    gold = Gold(0, Cube.SIZE * 2, Cube.SIZE)
    gold2 = Gold(0, Cube.SIZE * 4, Cube.SIZE)
    gold2.amount = 7

    woman = NPC("woman", Cube.SIZE * 5, Cube.SIZE * 7, Cube.SIZE)
    woman.on_interact = partial(display_text, game, "Hello !")

    boy = NPC("boy", Cube.SIZE * 4, Cube.SIZE * 9, Cube.SIZE)

    game.level.add_drawable(pot)
    game.level.add_drawable(pot2)
    game.level.add_drawable(chest)
    game.level.add_drawable(gold)
    game.level.add_drawable(gold2)
    game.level.add_drawable(woman)
    game.level.add_drawable(boy)
    game.level.add_drawable(game.hero)

    chest.id = 1
    chest.on_interact = partial(on_open_chest_1, game)

    event = Event(0, Cube.SIZE * 9, Cube.SIZE)
    event.on_intersect = partial(warp, game, 100, 100, 96)
    game.level.events.append(event)


def level_2(game):
    game.level.clear()
    game.level.read("data/level_2.map")

    gold = Gold(Cube.SIZE * 2, Cube.SIZE * 2, Cube.SIZE)
    gold.amount = 20
    game.level.add_drawable(gold)
    game.level.add_drawable(game.hero)
