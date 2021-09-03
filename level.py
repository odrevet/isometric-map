import pygame
from pygame.locals import *
import csv
import time

TILE_SIZE = 8

def cartesian_to_isometric(coord):
    return [coord[0] - coord[1], (coord[0] + coord[1]) // 2]


def to_2d_coords(index, width):
    return [index % width, index // width]


class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mapdata = []
        self.image_tileset = pygame.image.load("res/tileset.png")
        self.size = [0, 0]
        self.nb_floors = 0
    def read(self, filename):
        with open(filename, newline="") as file:
            reader = csv.reader(file, delimiter=",")
            level = []
            for row in reader:
                level.append(row[:])

        x, y, z = 0, 0, 0

        self.mapdata.append([])  # first floor
        for row in level:
            if row[0] == "-":
                self.mapdata.append([])  # append a floor
                x, y = 0, 0
                z += 1
                continue

            self.mapdata[z].append([])
            for tile in row:
                if x > self.size[0]:
                    self.size[0] = x
                if y > self.size[1]:
                    self.size[1] = y
 
                self.mapdata[z][y].append([])
                if tile:
                    for index in tile.split(","):
                        if index:
                            self.mapdata[z][y][x].append(
                                to_2d_coords(
                                    int(index),
                                    self.image_tileset.get_width() / TILE_SIZE,
                                )
                            )
                        else:
                            self.mapdata[z][y][x].append(None)
                else:
                    self.mapdata[z][y][x] = None
                x += 1
            y += 1
            x = 0

        self.size[0] += self.size[0]
        self.size[1] += self.size[1]        
        self.nb_floors = z + 1

    def cube_draw(self, surface_display, image_tileset, x, y, tile):
        top, left, right = tile

        if top is not None:
            surface_display.blit(
                image_tileset,
                (x, y),
                (top[0] * TILE_SIZE, top[1] * TILE_SIZE, TILE_SIZE * 4, TILE_SIZE * 2),
            )
        if left is not None:
            surface_display.blit(
                image_tileset,
                (x, y + TILE_SIZE),
                (
                    left[0] * TILE_SIZE,
                    left[1] * TILE_SIZE,
                    TILE_SIZE * 2,
                    TILE_SIZE * 3,
                ),
            )
        if right is not None:
            surface_display.blit(
                image_tileset,
                (x + TILE_SIZE * 2, y + TILE_SIZE),
                (
                    right[0] * TILE_SIZE,
                    right[1] * TILE_SIZE,
                    TILE_SIZE * 2,
                    TILE_SIZE * 3,
                ),
            )

    def draw(self, hero, camera, surface_display):
        hero_iso_x, hero_iso_y = cartesian_to_isometric((hero.x, hero.y))
        hero_index_x = (hero.x + 14) // (TILE_SIZE * 2)
        hero_index_y = (hero.y + 22) // (TILE_SIZE * 3)
        hero_index_z = hero.z // (TILE_SIZE * 3)

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.nb_floors):
                    try:
                        if self.mapdata[z][y][x] is not None:
                            self.cube_draw(
                                surface_display,
                                self.image_tileset,
                                camera[0] + x * TILE_SIZE * 2 - y * TILE_SIZE * 2,
                                camera[1]
                                + x * TILE_SIZE
                                + y * TILE_SIZE
                                - (TILE_SIZE * 2 * z),
                                self.mapdata[z][y][x],
                            )

                        if hero_index_x == x and hero_index_y == y:
                            surface_display.blit(
                                hero.image,
                                (
                                    camera[0] + hero_iso_x,
                                    camera[1] + hero_iso_y - hero.z - 32,
                                ),
                            )
                    except IndexError: 
                        pass

                    # time.sleep(0.5)
                    # pygame.display.update()

        if __debug__:
            blx, bly = cartesian_to_isometric((hero.x + TILE_SIZE, hero.y + TILE_SIZE))
            brx, bry = cartesian_to_isometric((hero.x + TILE_SIZE * 3, hero.y + TILE_SIZE))

            pygame.draw.line(
                surface_display,
                (255, 0, 0),
                (blx + camera[0], bly + camera[1]),
                (brx + camera[0], bry + camera[1]),
            )
