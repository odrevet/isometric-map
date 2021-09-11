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
                if hero.x > 0:
                    hero.x -= 1
            if event.key == pygame.K_RIGHT:
                hero.direction = Direction.RIGHT
                next_x = hero.x + 1
                tr = next_x + hero.size, hero.y
                br = next_x + hero.size, hero.y + hero.size
                if (
                    math.ceil(next_x / (CUBE_SIZE)) < level.size[0]
                    and level.tile(tr[0] // CUBE_SIZE, (tr[1]) // CUBE_SIZE, 1) is None
                    and level.tile((br[0] - 1) // CUBE_SIZE, (br[1] - 1) // CUBE_SIZE, 1)
                    is None
                ):
                    hero.x = next_x
            if event.key == pygame.K_UP:
                hero.direction = Direction.UP
                if hero.y > 0:
                    hero.y -= 1
            if event.key == pygame.K_DOWN:
                hero.direction = Direction.DOWN
                next_y = hero.y + 1
                bl = hero.x, next_y + hero.size
                br = hero.x + hero.size, next_y + hero.size
                if (
                    math.ceil(next_y / (CUBE_SIZE)) < level.size[1]
                    and level.tile(bl[0] // CUBE_SIZE, (bl[1]) // CUBE_SIZE, 1) is None
                    and level.tile((br[0] - 1) // CUBE_SIZE, (br[1]) // CUBE_SIZE, 1)
                    is None
                ):
                    hero.y = next_y
            if event.key == pygame.K_SPACE:
                hero.z += 1

        if __debug__:
            textsurface = font.render(
                f"Level size {level.size[0]}:{level.size[1]}:{level.size[2]}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 0))

            [bl, br, tl, tr] = hero.get_coords()
            textsurface = font.render(
                f"bl {bl} br {br} tl {tl} tr {tr}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 1))

            textsurface = font.render(
                f"bl ({(bl[0]) // 16}, {(bl[1] - 1) // 16})",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 2))

        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()
