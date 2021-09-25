import math

import pygame
from pygame.locals import *

import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox

from hero import Direction, Hero
from pot import Pot
from chest import Chest
from gold import Gold
from level import *
from cube import Cube
from point2d import Point2d


def hero_on_ground(hero, level):
    return (
        level.get_cube(
            bl.x // Cube.SIZE, bl.y // Cube.SIZE, (hero.position.z - 1) // Cube.SIZE
        )
        is not None
        or level.get_cube(
            br.x // Cube.SIZE, br.y // Cube.SIZE, (hero.position.z - 1) // Cube.SIZE
        )
        is not None
        or level.get_cube(
            tl.x // Cube.SIZE, tl.y // Cube.SIZE, (hero.position.z - 1) // Cube.SIZE
        )
        is not None
        or level.get_cube(
            tr.x // Cube.SIZE, tr.y // Cube.SIZE, (hero.position.z - 1) // Cube.SIZE
        )
        is not None
    )


# init pygame
pygame.init()
bgcolor = (0, 0, 0)

resolution_screen = Point2d(320, 240)
resolution_window = Point2d(640, 480)
surface_window = pygame.display.set_mode(resolution_window.list())
surface_screen = pygame.Surface(resolution_screen.list())
pygame.display.set_caption("Isometric map")
clock = pygame.time.Clock()
camera = Point2d(resolution_screen.x // 2, resolution_screen.y // 2)

# init GUI
ui_manager = pygame_gui.UIManager(resolution_screen.list(), "data/themes/classic.json")
debug_textbox = UITextBox(
    "",
    pygame.Rect((0, 0), (320, 35)),
    manager=ui_manager,
    object_id="#debug_textbox",
)

# Music
pygame.mixer.music.load("res/music/overworld_2.mid")
pygame.mixer.music.play()

# init level
level = Level()
level.read("data/level.map")

# init hero
hero = Hero(z=Cube.SIZE)

# create drawables
pot = Pot(Cube.SIZE, Cube.SIZE, Cube.SIZE * 3)
chest = Chest(Cube.SIZE * 2, 0, Cube.SIZE)
gold = Gold(Cube.SIZE * 3, 0, Cube.SIZE)

# drawables
drawables = []
drawables.append(hero)
drawables.append(pot)
drawables.append(chest)
drawables.append(gold)


while True:
    # logic
    time_delta = clock.tick(60) / 1000.0
    [bl, br, tl, tr] = hero.get_coords()
    hero.on_ground = hero_on_ground(hero, level)
    hero.zindex = sum(list(map((lambda x: x // Cube.SIZE), hero.position.list())))
    pot.zindex = sum(list(map((lambda x: x // Cube.SIZE), pot.position.list())))

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

            if event.key == pygame.K_LEFT:
                hero.is_moving = True
                hero.direction = Direction.LEFT
            if event.key == pygame.K_RIGHT:
                hero.is_moving = True
                hero.direction = Direction.RIGHT
            if event.key == pygame.K_UP:
                hero.is_moving = True
                hero.direction = Direction.UP
            if event.key == pygame.K_DOWN:
                hero.is_moving = True
                hero.direction = Direction.DOWN

            if event.key == pygame.K_SPACE:
                if hero.on_ground:
                    hero.jump = True
        elif event.type == KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                hero.is_moving = False

    # update hero location
    if hero.is_moving:
        if hero.direction == Direction.UP:
            if (
                hero.position.y - 1 >= 0
                and level.get_cube(
                    tl.x // Cube.SIZE,
                    (tl.y - 1) // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
                and level.get_cube(
                    tr.x // Cube.SIZE,
                    (tr.y - 1) // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
            ):
                hero.position.y -= 1
        elif hero.direction == Direction.RIGHT:
            if (
                math.ceil((hero.position.x + 1) / (Cube.SIZE)) < level.size.x
                and level.get_cube(
                    (tr.x + 1) // Cube.SIZE,
                    tr.y // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
                and level.get_cube(
                    (br.x + 1) // Cube.SIZE,
                    br.y // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
            ):
                hero.position.x += 1
        elif hero.direction == Direction.DOWN:
            if (
                math.ceil((hero.position.y + 1) / (Cube.SIZE)) < level.size.y
                and level.get_cube(
                    bl.x // Cube.SIZE,
                    (bl.y + 1) // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
                and level.get_cube(
                    br.x // Cube.SIZE,
                    (br.y + 1) // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
            ):
                hero.position.y += 1
        elif hero.direction == Direction.LEFT:
            if (
                hero.position.x - 1 >= 0
                and level.get_cube(
                    (tl.x - 1) // Cube.SIZE,
                    tl.y // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
                and level.get_cube(
                    (bl.x - 1) // Cube.SIZE,
                    bl.y // Cube.SIZE,
                    hero.position.z // Cube.SIZE,
                )
                is None
            ):
                hero.position.x -= 1

    # jump
    if hero.jump == True:
        if hero.jump_cur >= hero.jump_max:
            hero.jump = False
            hero.jump_cur = 0
        else:
            hero.position.z += 1
            hero.jump_cur += 1

    # gravity
    if hero.jump == False and not hero.on_ground:
        hero.position.z -= 1

    # draw
    surface_screen.fill(bgcolor)
    level.draw(drawables, camera, surface_screen)

    # debug
    if __debug__:
        debug_text = f"{level.size.x}:{level.size.y}:{level.size.z} {hero.position.x}:{hero.position.y}:{hero.position.z}"
        debug_textbox.html_text = debug_text
        debug_textbox.rebuild()
        ui_manager.draw_ui(surface_screen)

        # draw lines around hero
        # get hero coords and find isometric locations
        bl, br, tl, tr = list(
            map(
                (lambda coord: cartesian_to_isometric(coord.list())),
                hero.get_coords(),
            )
        )

        # adjust all point with camera and hero z position
        points = list(
            map(
                (
                    lambda point: (
                        point.x + camera.x,
                        point.y + camera.y - hero.position.z + Cube.SIZE,
                    )
                ),
                [bl, br, br, tr, tl, tr, tl, bl],
            )
        )

        pygame.draw.lines(
            surface_screen,
            (255, 255, 255),
            False,
            points,
        )

    ui_manager.update(time_delta)

    # stretch display
    scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
    surface_window.blit(scaled_win, (0, 0))

    pygame.display.update()
