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
                walkable = True
                try:
                    br = [hero.x + (TILE_SIZE * 2), hero.y + (TILE_SIZE * 2)]
                    br[0] += 1
                    br_index_x = math.ceil((br[0]) / (TILE_SIZE * 2) - 1)
                    br_index_y = math.ceil((br[1]) / (TILE_SIZE * 2) - 1)

                    walkable = not isinstance(
                        level.mapdata[1][br_index_y][br_index_x], list
                    )
                except IndexError:
                    pass
                if (
                    math.ceil((hero.x + 1) / (TILE_SIZE * 2)) < level.size[0]
                    and walkable
                ):
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

            hero_index = hero.get_index()
            textsurface = font.render(
                f"x {hero_index[0]} y {hero_index[1]} z {hero_index[2]} | x {hero.x} y {hero.y} z {hero.z}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 1))

            textsurface = font.render(
                f"x {hero.x + (TILE_SIZE * 2) - 1} {math.ceil((hero.x + (TILE_SIZE * 2)) / (TILE_SIZE * 2) ) - 1} y {hero.y + (TILE_SIZE * 2) - 1} {math.ceil((hero.y + (TILE_SIZE * 2)) / (TILE_SIZE * 2) ) - 1}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 2))

        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()
