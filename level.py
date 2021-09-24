import pygame
from pygame.locals import *
import csv

from hero import Hero
from cube import Cube
from const import *
from point3d import Point3d
from utils import *


class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 3d array of Cubes
        self.mapdata = []

        self.image_tileset = pygame.image.load("res/tileset.png")
        self.size = Point3d()

    def read(self, filename):
        with open(filename, newline="") as file:
            reader = csv.reader(file, delimiter=",")
            level = []
            for row in reader:
                level.append(row[:])

        position = Point3d()

        self.mapdata.append([])  # first floor
        for row in level:
            if row[0] == "-":
                self.mapdata.append([])  # append a floor
                position.x, position.y = 0, 0
                position.z += 1
                continue

            self.mapdata[position.z].append([])
            for tile in row:
                if position.x > self.size.x:
                    self.size.x = position.x
                if position.y > self.size.y:
                    self.size.y = position.y

                self.mapdata[position.z][position.y].append([])
                if tile:
                    coords = []
                    for index in tile.split(","):
                        if index:
                            coords.append(
                                to_2d_coords(
                                    int(index),
                                    self.image_tileset.get_width() / TILE_SIZE,
                                )
                            )
                        else:
                            coords.append(None)
                    cube = Cube(coords)
                    cube.position = Point3d(position.x, position.y, position.z)
                    self.mapdata[position.z][position.y][position.x] = cube
                else:
                    self.mapdata[position.z][position.y][position.x] = None
                position.x += 1
            position.y += 1
            position.x = 0

        self.size.x += 1
        self.size.y += 1
        self.size.z = position.z + 1

    def get_cube(self, x, y, z):
        try:
            return self.mapdata[z][y][x]
        except IndexError:
            print(f"No Cube at {x}:{y}:{z}")
            pass

    def draw(self, hero, camera, surface_display):
        hero_iso = cartesian_to_isometric((hero.position.x, hero.position.y))

        # object, zindex, is_hero_top
        drawables = []

        # top
        drawables.append(
            (
                hero,
                hero.zindex + 1,
                True,
            )
        )

        # bottom
        drawables.append(
            (
                hero,
                hero.zindex,
                False,
            )
        )

        hero_width = 32
        hero_height = 48
        surface_tmp = pygame.Surface((hero_width, hero_height), pygame.SRCALPHA)
        hero.draw(0, 0, surface_tmp)

        for z in range(self.size.z):
            for y in range(self.size.y):
                for x in range(self.size.x):
                    if self.mapdata[z][y][x] is not None:
                        self.mapdata[z][y][x].zindex = x + y + z
                        drawables.append(
                            (
                                self.mapdata[z][y][x],
                                self.mapdata[z][y][x].zindex,
                            )
                        )

        for drawable in sorted(drawables, key=lambda x: x[1]):
            if isinstance(drawable[0], Hero):
                if drawable[2] == True:
                    # blit hero top
                    surface_display.blit(
                        surface_tmp,
                        (
                            camera.x + hero_iso.x - Cube.SIZE,
                            camera.y + hero_iso.y - hero.position.z - Cube.SIZE,
                        ),
                        (0, 0, hero_width, hero_height // 2),
                    )
                else:
                    # blit hero bottom
                    surface_display.blit(
                        surface_tmp,
                        (
                            camera.x + hero_iso.x - Cube.SIZE,
                            camera.y
                            + hero_iso.y
                            - hero.position.z
                            - Cube.SIZE
                            + hero_height // 2,
                        ),
                        (0, hero_height // 2, hero_width, hero_height // 2),
                    )
            else:
                drawable[0].draw(
                    surface_display,
                    self.image_tileset,
                    camera.x
                    + drawable[0].position.x * Cube.SIZE
                    - drawable[0].position.y * Cube.SIZE
                    - Cube.SIZE,
                    camera.y
                    + drawable[0].position.x * TILE_SIZE
                    + drawable[0].position.y * TILE_SIZE
                    - (Cube.SIZE * drawable[0].position.z),
                )

        if __debug__:
            # draw lines around hero
            # get hero coords and find isometric locations
            bl, br, tl, tr = list(
                map(
                    (lambda coord: cartesian_to_isometric(coord.list())),
                    hero.get_coords(),
                )
            )

            # adjust all point with camera and hero z position
            points = list(
                map(
                    (
                        lambda point: (
                            point.x + camera.x,
                            point.y + camera.y - hero.position.z + Cube.SIZE,
                        )
                    ),
                    [bl, br, br, tr, tl, tr, tl, bl],
                )
            )

            pygame.draw.lines(
                surface_display,
                (255, 255, 255),
                False,
                points,
            )
