import pygame
from pygame.locals import *
import csv

TILE_SIZE = 8


def to_2d_coords(index, width):
    return [index % width, index // width]


def read_level(filename, tileset_width):
    with open(filename, newline="") as file:
        reader = csv.reader(file, delimiter=",")
        level = []
        for row in reader:
            level.append(row[:])

    data = []
    x, y, z = 0, 0, 0

    data.append([])  # first floor
    for row in level:
        if row[0] == "-":
            data.append([])  # append a floor
            x, y = 0, 0
            z += 1
            continue

        data[z].append([])
        for tile in row:
            data[z][y].append([])
            if tile:
                for index in tile.split(","):
                    if index:
                        data[z][y][x].append(to_2d_coords(int(index), tileset_width))
                    else:
                        data[z][y][x].append(None)
            else:
                data[z][y][x] = None
            x += 1
        y += 1
        x = 0

    return data


def cube_draw(surface_display, image_tileset, x, y, tile):
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
            (left[0] * TILE_SIZE, left[1] * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE * 3),
        )
    if right is not None:
        surface_display.blit(
            image_tileset,
            (x + TILE_SIZE * 2, y + TILE_SIZE),
            (right[0] * TILE_SIZE, right[1] * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE * 3),
        )


def level_draw(level, image_tileset, camera, surface_display):
    size = [3, 2]
    hm = [[1, 2, 0], [1, 1, 1]]
    for x in range(size[0]):
        for y in range(size[1]):
            for z in range(hm[y][x]):
                print(z, x, y)
                if level[z][y][x] is not None:
                    cube_draw(
                        surface_display,
                        image_tileset,
                        camera[0] + x * TILE_SIZE * 2 - y * TILE_SIZE * 2,
                        camera[1] + x * TILE_SIZE + y * TILE_SIZE - (TILE_SIZE * 2 * z),
                        level[z][y][x],
                    )
