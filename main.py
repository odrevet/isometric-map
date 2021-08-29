import pygame
from pygame.locals import *

from hero import Hero
from level import *

def cartesian_to_isometric(coord):
    return [coord[0] - coord[1], (coord[0] + coord[1]) // 2]

pygame.init()
bgcolor = (0, 0, 0)
screen_res = (640, 480)
surface_display = pygame.display.set_mode(screen_res)
pygame.display.set_caption('Isometric map')
pygame.key.set_repeat(1, 16)

image_tileset = pygame.image.load('res/tileset.png')
level = read_level('data/level.map', image_tileset.get_width() / TILE_SIZE)

hero = Hero()
camera = [screen_res[0] / 2, screen_res[1] / 2]

clock = pygame.time.Clock()

while True :
    hero_index_x = hero.x // (TILE_SIZE * 2)
    hero_index_y = hero.y // (TILE_SIZE * 2)
    hero_index_z = hero.z // (TILE_SIZE * 2)

    surface_display.fill(bgcolor)

    level_draw(level, image_tileset, camera, surface_display)
    hero_iso_x, hero_iso_y = cartesian_to_isometric((hero.x, hero.y))
    surface_display.blit(hero.image, (camera[0] + hero_iso_x , camera[1] + hero_iso_y - hero.z - 32))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
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
                if hero.x + TILE_SIZE * 2 < len(level[hero_index_z][hero_index_y] * TILE_SIZE * 2) - 1:
                    hero.x += 1
            if event.key == pygame.K_UP:
                if hero.y > 0: 
                    hero.y -= 1
            if event.key == pygame.K_DOWN:
                if hero.y + TILE_SIZE * 2 < len(level[hero_index_z] * TILE_SIZE * 2) - 1:
                    hero.y += 1
            if event.key == pygame.K_SPACE:
                hero.z+= 1

        pygame.display.update()
        clock.tick(60)
