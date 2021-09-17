import pygame
from pygame import surface
from pygame.locals import *
import csv
from hero import Hero

from const import *
from functools import cmp_to_key

def cartesian_to_isometric(coord):
    return [coord[0] - coord[1], (coord[0] + coord[1]) // 2]


def to_2d_coords(index, width):
    return [index % width, index // width]

def compare(item1, item2):
    a = item1[0]
    b = item2[0]
    if b[0] > a[0] or b[1] > a[1]:
        return -1
    return 1

class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mapdata = []
        self.image_tileset = pygame.image.load("res/tileset.png")
        self.size = [0, 0, 0]

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

        self.size[0] += 1
        self.size[1] += 1
        self.size[2] = z + 1

    def tile(self, x, y, z):
        try:
            return self.mapdata[z][y][x]
        except IndexError:
            print(f"Index error at {x}:{y}:{z}")
            pass

    def cube_draw(self, surface_display, image_tileset, x, y, tile):
        top, left, right = tile

        if top is not None:
            surface_display.blit(
                image_tileset,
                (x, y),
                (top[0] * TILE_SIZE, top[1] * TILE_SIZE, CUBE_SIZE * 2, CUBE_SIZE),
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
        hero_index = hero.get_index()

        for z in range(self.size[2]):
            drawables = []
            if hero_index[2]== z:
                drawables.append(((hero.x // CUBE_SIZE, hero.y // CUBE_SIZE, hero.z // CUBE_SIZE), hero))

            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    if self.mapdata[z][y][x] is not None:
                        drawables.append(((x, y, z), self.mapdata[z][y][x]))

            for drawable in sorted(drawables, key=cmp_to_key(compare)):
                if isinstance(drawable[1], Hero):
                    hero.draw(
                        camera[0] + hero_iso_x - CUBE_SIZE,
                        camera[1] + hero_iso_y - hero.z - CUBE_SIZE,
                        surface_display,
                    )
                else:
                    self.cube_draw(
                        surface_display,
                        self.image_tileset,
                        camera[0]
                        + drawable[0][0] * CUBE_SIZE
                        - drawable[0][1] * CUBE_SIZE
                        - CUBE_SIZE,
                        camera[1]
                        + drawable[0][0] * TILE_SIZE
                        + drawable[0][1] * TILE_SIZE
                        - (CUBE_SIZE * drawable[0][2]),
                        drawable[1],
                    )               

        if __debug__:
            bl, br, tl, tr = hero.get_coords()
            bl = cartesian_to_isometric(bl)
            br = cartesian_to_isometric(br)
            tl = cartesian_to_isometric(tl)
            tr = cartesian_to_isometric(tr)

            points = [
                (bl[0] + camera[0], bl[1] + camera[1] - hero.z + CUBE_SIZE),
                (br[0] + camera[0], br[1] + camera[1] - hero.z + CUBE_SIZE),
                (br[0] + camera[0], br[1] + camera[1] - hero.z + CUBE_SIZE),
                (tr[0] + camera[0], tr[1] + camera[1] - hero.z + CUBE_SIZE),
                (tl[0] + camera[0], tl[1] + camera[1] - hero.z + CUBE_SIZE),
                (tr[0] + camera[0], tr[1] + camera[1] - hero.z + CUBE_SIZE),
                (tl[0] + camera[0], tl[1] + camera[1] - hero.z + CUBE_SIZE),
                (bl[0] + camera[0], bl[1] + camera[1] - hero.z + CUBE_SIZE),
            ]
            pygame.draw.lines(
                surface_display,
                (255, 255, 255),
                False,
                points,
            )
