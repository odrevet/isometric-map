import math

import pygame
from pygame.locals import *

import pygame_gui
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.core import IncrementalThreadedResourceLoader
from pygame_gui import UI_TEXT_BOX_LINK_CLICKED

from hero import Direction, Hero
from level import *


def hero_on_ground(hero, level):
    return (
        level.tile(
            bl[0] // CUBE_SIZE, bl[1] // CUBE_SIZE, (hero.position.z - 1) // CUBE_SIZE
        )
        is not None
        or level.tile(
            br[0] // CUBE_SIZE, br[1] // CUBE_SIZE, (hero.position.z - 1) // CUBE_SIZE
        )
        is not None
        or level.tile(
            tl[0] // CUBE_SIZE, tl[1] // CUBE_SIZE, (hero.position.z - 1) // CUBE_SIZE
        )
        is not None
        or level.tile(
            tr[0] // CUBE_SIZE, tr[1] // CUBE_SIZE, (hero.position.z - 1) // CUBE_SIZE
        )
        is not None
    )


# init pygame
pygame.init()
pygame.font.init()
font_size = 24
font = pygame.font.SysFont("", font_size)
bgcolor = (0, 0, 0)

resolution_screen = (320, 240)
resolution_window = (640, 480)
surface_window = pygame.display.set_mode(resolution_window)
surface_screen = pygame.Surface(resolution_screen)
pygame.display.set_caption("Isometric map")
clock = pygame.time.Clock()
camera = [resolution_screen[0] / 2, resolution_screen[1] / 2]

# init GUI
ui_manager = pygame_gui.UIManager(resolution_screen, "data/themes/classic.json")
debug_textbox = UITextBox(
    '',
    pygame.Rect((0, 0), (320, 70)),
    manager=ui_manager,
    object_id="#debug_textbox",
)

# init level
level = Level()
level.read("data/level.map")

# init hero
hero = Hero()


while True:
    # logic
    time_delta = clock.tick(60) / 1000.0
    [bl, br, tl, tr] = hero.get_coords()
    hero.on_ground = hero_on_ground(hero, level)
    hero.zindex = (
        hero.position.x / CUBE_SIZE
        + hero.position.y / CUBE_SIZE
        + hero.position.z / CUBE_SIZE
    )

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
                and level.tile(
                    tl[0] // CUBE_SIZE,
                    (tl[1] - 1) // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
                )
                is None
                and level.tile(
                    tr[0] // CUBE_SIZE,
                    (tr[1] - 1) // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
                )
                is None
            ):
                hero.position.y -= 1
        elif hero.direction == Direction.RIGHT:
            if (
                math.ceil((hero.position.x + 1) / (CUBE_SIZE)) < level.size[0]
                and level.tile(
                    (tr[0] + 1) // CUBE_SIZE,
                    tr[1] // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
                )
                is None
                and level.tile(
                    (br[0] + 1) // CUBE_SIZE,
                    br[1] // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
                )
                is None
            ):
                hero.position.x += 1
        elif hero.direction == Direction.DOWN:
            if (
                math.ceil((hero.position.y + 1) / (CUBE_SIZE)) < level.size[1]
                and level.tile(
                    bl[0] // CUBE_SIZE,
                    (bl[1] + 1) // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
                )
                is None
                and level.tile(
                    br[0] // CUBE_SIZE,
                    (br[1] + 1) // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
                )
                is None
            ):
                hero.position.y += 1
        elif hero.direction == Direction.LEFT:
            if (
                hero.position.x - 1 >= 0
                and level.tile(
                    (tl[0] - 1) // CUBE_SIZE,
                    tl[1] // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
                )
                is None
                and level.tile(
                    (bl[0] - 1) // CUBE_SIZE,
                    bl[1] // CUBE_SIZE,
                    hero.position.z // CUBE_SIZE,
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
    level.draw(hero, camera, surface_screen)

    # debug
    if __debug__:
        debug_text = f"Level size {level.size[0]}:{level.size[1]}:{level.size[2]} <br/>"
        debug_text += f"x {hero.position.x} y {hero.position.y} z {hero.position.z}<br/>jump {hero.jump} ground {hero.on_ground}"
        debug_textbox.html_text = debug_text
        debug_textbox.rebuild()
        ui_manager.draw_ui(surface_screen)


    ui_manager.update(time_delta)

    # stretch display
    scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
    surface_window.blit(scaled_win, (0, 0))

    pygame.display.update()
