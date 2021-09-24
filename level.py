import pygame
from pygame.locals import *
import csv

from hero import Hero
from cube import Cube
from const import *
from point3d import Point3d
from utils import *
from drawable_chunk import DrawableChunk


class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cubes = []
        self.image_tileset = pygame.image.load("res/tileset.png")
        self.size = Point3d()

    def read(self, filename):
        with open(filename, newline="") as file:
            reader = csv.reader(file, delimiter=",")
            level = []
            for row in reader:
                level.append(row[:])

        position = Point3d()

        self.cubes.append([])  # first floor
        for row in level:
            if row[0] == "-":
                self.cubes.append([])  # append a floor
                position.x, position.y = 0, 0
                position.z += 1
                continue

            self.cubes[position.z].append([])
            for tile in row:
                if position.x > self.size.x:
                    self.size.x = position.x
                if position.y > self.size.y:
                    self.size.y = position.y

                self.cubes[position.z][position.y].append([])
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
                    self.cubes[position.z][position.y][position.x] = cube
                else:
                    self.cubes[position.z][position.y][position.x] = None
                position.x += 1
            position.y += 1
            position.x = 0

        self.size.x += 1
        self.size.y += 1
        self.size.z = position.z + 1

    def get_cube(self, x, y, z):
        try:
            return self.cubes[z][y][x]
        except IndexError:
            print(f"No Cube at {x}:{y}:{z}")
            pass

    def draw(self, drawables_sprites, camera, surface_display):
        # Work In Progress: split drawables into chunks when needed
        drawables = []
        if len(drawables_sprites) > 0:
            hero = drawables_sprites[0]
            hero_top = DrawableChunk(hero.position.x, hero.position.y, hero.position.z)
            hero_top.zindex = (
                sum(list(map((lambda x: x / Cube.SIZE), hero_top.position.list()))) + 1
            )
            hero_top.number = 0
            hero_bottom = DrawableChunk(
                hero.position.x, hero.position.y, hero.position.z
            )
            hero_bottom.zindex = sum(
                list(map((lambda x: x / Cube.SIZE), hero_bottom.position.list()))
            )
            hero_bottom.number = 1
            drawables.append(hero_top)
            drawables.append(hero_bottom)
            hero_width = 32
            hero_height = 48
            surface_tmp = pygame.Surface((hero_width, hero_height), pygame.SRCALPHA)
            hero.draw(0, 0, surface_tmp)

        for z in range(self.size.z):
            for y in range(self.size.y):
                for x in range(self.size.x):
                    if self.cubes[z][y][x] is not None:
                        self.cubes[z][y][x].zindex = x + y + z
                        drawables.append(self.cubes[z][y][x])

        for drawable in sorted(drawables, key=lambda drawable: drawable.zindex):
            if isinstance(drawable, Cube):
                drawable.draw(
                    surface_display,
                    self.image_tileset,
                    camera.x
                    + drawable.position.x * Cube.SIZE
                    - drawable.position.y * Cube.SIZE
                    - Cube.SIZE,
                    camera.y
                    + drawable.position.x * TILE_SIZE
                    + drawable.position.y * TILE_SIZE
                    - (Cube.SIZE * drawable.position.z),
                )
            elif isinstance(drawable, DrawableChunk):
                drawable_iso = cartesian_to_isometric(
                    (drawable.position.x, drawable.position.y)
                )

                z_shift = (hero_height // 2) * drawable.number
                surface_display.blit(
                    surface_tmp,
                    (
                        camera.x + drawable_iso.x - Cube.SIZE,
                        camera.y
                        + drawable_iso.y
                        - drawable.position.z
                        - Cube.SIZE
                        + z_shift,
                    ),
                    (0, z_shift, hero_width, hero_height // 2),
                )
