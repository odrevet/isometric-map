import pygame
from pygame.locals import *
import math

from hero import Hero
from level import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("", 30)
bgcolor = (0, 0, 0)
screen_res = (640, 480)
surface_display = pygame.display.set_mode(screen_res)
pygame.display.set_caption("Isometric map")
pygame.key.set_repeat(1, 24)

level = Level()
level.read("data/level.map")

hero = Hero()
camera = [screen_res[0] / 2, screen_res[1] / 2]

while True:
    surface_display.fill(bgcolor)
    level.draw(hero, camera, surface_display)

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
                if math.ceil((hero.x) / (TILE_SIZE * 2)) < level.size[0]:
                    hero.x += 1
            if event.key == pygame.K_UP:
                if hero.y > 0:
                    hero.y -= 1
            if event.key == pygame.K_DOWN:
                if math.ceil((hero.y) / (TILE_SIZE * 2)) < level.size[1]:
                    hero.y += 1
            if event.key == pygame.K_SPACE:
                hero.z += 1

        if __debug__:
            hero_index = hero.get_index()
            textsurface = font.render(
                f"Index: x {hero_index[0]} y {hero_index[1]} z {hero_index[2]} | Coords: x {hero.x} y {hero.y} z {hero.z}",
                False,
                (255, 255, 255),
            )
            surface_display.blit(textsurface, (0, 0))
        pygame.display.update()
