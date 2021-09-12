import pygame
from pygame.locals import *
import math

from hero import Direction, Hero
from level import *


def hero_on_ground(hero, level):
    return (
        level.tile(bl[0] // CUBE_SIZE, bl[1] // CUBE_SIZE, (hero.z - 1) // CUBE_SIZE)
        is not None
        or level.tile(br[0] // CUBE_SIZE, br[1] // CUBE_SIZE, (hero.z - 1) // CUBE_SIZE)
        is not None
        or level.tile(tl[0] // CUBE_SIZE, tl[1] // CUBE_SIZE, (hero.z - 1) // CUBE_SIZE)
        is not None
        or level.tile(tr[0] // CUBE_SIZE, tr[1] // CUBE_SIZE, (hero.z - 1) // CUBE_SIZE)
        is not None
    )


pygame.init()
pygame.font.init()
font_size = 24
font = pygame.font.SysFont("", font_size)
bgcolor = (0, 0, 0)
resolution_window = (640, 480)
resolution_screen = (320, 240)
surface_window = pygame.display.set_mode(resolution_window)
surface_screen = pygame.Surface(resolution_screen)
pygame.display.set_caption("Isometric map")

level = Level()
level.read("data/level.map")

hero = Hero()
camera = [resolution_screen[0] / 2, resolution_screen[1] / 2]

clock = pygame.time.Clock()

while True:
    time_delta = clock.tick(60) / 1000.0
    surface_screen.fill(bgcolor)
    level.draw(hero, camera, surface_screen)
    [bl, br, tl, tr] = hero.get_coords()

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
                if hero_on_ground(hero, level):
                    hero.jump = True
        elif event.type == KEYUP:
            hero.is_moving = False

    # update hero location
    if hero.is_moving:
        if hero.direction == Direction.UP:
            if (
                hero.y - 1 >= 0
                and level.tile(
                    tl[0] // CUBE_SIZE, (tl[1] - 1) // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
                and level.tile(
                    tr[0] // CUBE_SIZE, (tr[1] - 1) // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
            ):
                hero.y -= 1
        elif hero.direction == Direction.RIGHT:
            if (
                math.ceil((hero.x + 1) / (CUBE_SIZE)) < level.size[0]
                and level.tile(
                    (tr[0] + 1) // CUBE_SIZE, tr[1] // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
                and level.tile(
                    (br[0] + 1) // CUBE_SIZE, br[1] // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
            ):
                hero.x += 1
        elif hero.direction == Direction.DOWN:
            if (
                math.ceil((hero.y + 1) / (CUBE_SIZE)) < level.size[1]
                and level.tile(
                    bl[0] // CUBE_SIZE, (bl[1] + 1) // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
                and level.tile(
                    br[0] // CUBE_SIZE, (br[1] + 1) // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
            ):
                hero.y += 1
        elif hero.direction == Direction.LEFT:
            if (
                hero.x - 1 >= 0
                and level.tile(
                    (tl[0] - 1) // CUBE_SIZE, tl[1] // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
                and level.tile(
                    (bl[0] - 1) // CUBE_SIZE, bl[1] // CUBE_SIZE, hero.z // CUBE_SIZE
                )
                is None
            ):
                hero.x -= 1

    # jump
    if hero.jump == True:
        if hero.jump_cur >= hero.jump_max:
            hero.jump = False
            hero.jump_cur = 0
        else:
            hero.z += 1
            hero.jump_cur += 1

    # gravity
    if hero.jump == False and not hero_on_ground(hero, level):
        hero.z -= 1

    # debug
    if __debug__:
        textsurface = font.render(
            f"Level size {level.size[0]}:{level.size[1]}:{level.size[2]}",
            False,
            (255, 255, 255),
        )
        surface_screen.blit(textsurface, (0, font_size * 0))

        textsurface = font.render(
            f"x {hero.x} y {hero.y} z {hero.z} jump {hero.jump} ground {hero_on_ground(hero, level)}",
            False,
            (255, 255, 255),
        )
        surface_screen.blit(textsurface, (0, font_size * 1))

        textsurface = font.render(
            f"bl {bl} br {br} tl {tl} tr {tr}",
            False,
            (255, 255, 255),
        )
        surface_screen.blit(textsurface, (0, font_size * 2))

    scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
    surface_window.blit(scaled_win, (0, 0))
    pygame.display.update()
