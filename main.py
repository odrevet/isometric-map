import pygame
from pygame.locals import *
import math

from hero import Direction, Hero
from level import *

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
pygame.key.set_repeat(1, 24)

level = Level()
level.read("data/level.map")

hero = Hero()
camera = [resolution_screen[0] / 2, resolution_screen[1] / 2]

while True:
    surface_screen.fill(bgcolor)
    level.draw(hero, camera, surface_screen)
    [bl, br, tl, tr] = hero.get_coords()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

            if event.key == pygame.K_LEFT:
                hero.direction = Direction.LEFT
                next_x = hero.x - 1
                bl[0] -= 1
                tl[0] -= 1
                if (
                    next_x >= 0
                    and level.tile(tl[0] // CUBE_SIZE, tl[1] // CUBE_SIZE, 1) is None
                    and level.tile(bl[0] // CUBE_SIZE, bl[1] // CUBE_SIZE, 1) is None
                ):
                    hero.x = next_x
            if event.key == pygame.K_RIGHT:
                hero.direction = Direction.RIGHT
                next_x = hero.x + 1
                tr[0] += 1
                br[0] += 1
                if (
                    math.ceil(next_x / (CUBE_SIZE)) < level.size[0]
                    and level.tile(tr[0] // CUBE_SIZE, tr[1] // CUBE_SIZE, 1) is None
                    and level.tile(br[0] // CUBE_SIZE, br[1] // CUBE_SIZE, 1) is None
                ):
                    hero.x = next_x
            if event.key == pygame.K_UP:
                hero.direction = Direction.UP
                next_y = hero.y - 1
                tl[1] -= 1
                tr[1] -= 1
                if (
                    next_y >= 0
                    and level.tile(tl[0] // CUBE_SIZE, tl[1] // CUBE_SIZE, 1) is None
                    and level.tile(tr[0] // CUBE_SIZE, tr[1] // CUBE_SIZE, 1) is None
                ):
                    hero.y = next_y
            if event.key == pygame.K_DOWN:
                hero.direction = Direction.DOWN
                next_y = hero.y + 1
                bl[1] += 1
                br[1] += 1
                if (
                    math.ceil(next_y / (CUBE_SIZE)) < level.size[1]
                    and level.tile(bl[0] // CUBE_SIZE, bl[1] // CUBE_SIZE, 1) is None
                    and level.tile(br[0] // CUBE_SIZE, br[1] // CUBE_SIZE, 1) is None
                ):
                    hero.y = next_y
            if event.key == pygame.K_SPACE:
                hero.jump = True

        if hero.jump == True:
            if hero.jump_cur < hero.jump_max:
                hero.z += 1
                hero.jump_cur += 1

        if __debug__:
            textsurface = font.render(
                f"Level size {level.size[0]}:{level.size[1]}:{level.size[2]}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 0))

            textsurface = font.render(
                f"bl {bl} br {br} tl {tl} tr {tr}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 1))

        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()
