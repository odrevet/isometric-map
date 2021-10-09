from pot import Pot
from chest import Chest
from gold import Gold
from cube import Cube
from functools import partial

def clear(level):
    level.drawables = []
    level.cubes = []

def on_open_chest_1(game):
    game.hero.gold += 50

def level_1(game):
    clear(game.level)
    game.level.read("data/level.map")

    pot = Pot(Cube.SIZE * 6, Cube.SIZE * 5.5, Cube.SIZE)
    pot2 = Pot(Cube.SIZE * 6, Cube.SIZE * 3.5, Cube.SIZE)
    chest = Chest(Cube.SIZE * 2, Cube.SIZE * 6, Cube.SIZE)
    gold = Gold(0, Cube.SIZE * 2, Cube.SIZE)
    gold2 = Gold(0, Cube.SIZE * 4, Cube.SIZE)
    gold2.amount = 7

    game.level.add_drawable(pot)
    game.level.add_drawable(pot2)
    game.level.add_drawable(chest)
    game.level.add_drawable(gold)
    game.level.add_drawable(gold2)
    game.level.add_drawable(game.hero)

    chest.id = 1
    chest.on_open = partial(on_open_chest_1, game)


def level_2(game):
    clear(game.level)
    game.level.read("data/level_2.map")

    gold = Gold(Cube.SIZE * 2, Cube.SIZE * 2, Cube.SIZE)
    gold.amount = 20
    game.level.add_drawable(gold)
    game.level.add_drawable(game.hero)
