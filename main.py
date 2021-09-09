import pygame
from pygame.locals import *
import math

from pygame.sndarray import array

from hero import Hero
from level import *

pygame.init()
pygame.font.init()
font_size = 30
font = pygame.font.SysFont("", 28)
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
                if hero.x > 0:
                    hero.x -= 1
            if event.key == pygame.K_RIGHT:
                hero.x += 1
            if event.key == pygame.K_UP:
                if hero.y > 0:
                    hero.y -= 1
            if event.key == pygame.K_DOWN:
                if math.ceil((hero.y + 1) / (TILE_SIZE * 2)) < level.size[1]:
                    hero.y += 1
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

        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()
