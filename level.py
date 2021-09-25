import pygame
from pygame.locals import *
import csv

from drawable import Drawable
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

        for row in level:
            if row[0] == "-":
                position.x, position.y = 0, 0
                position.z += 1
                continue

            for tile in row:
                if position.x > self.size.x:
                    self.size.x = position.x
                if position.y > self.size.y:
                    self.size.y = position.y

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
                    cube.zindex = sum(cube.position.list())
                    self.cubes.append(cube)
                position.x += 1
            position.y += 1
            position.x = 0

        self.size.x += 1
        self.size.y += 1
        self.size.z = position.z + 1

    def get_cube(self, x, y, z):
        try:
            for i in range(len(self.cubes)):
                cube = self.cubes[i]
                if (
                    cube.position.x == x
                    and cube.position.y == y
                    and cube.position.z == z
                ):
                    return cube
        except IndexError:
            print(f"No Cube at {x}:{y}:{z}")
            pass

    def draw(self, drawables_sprites, camera, surface_display):
        drawables = []

        # Work In Progress: split drawables into chunks when needed
        for drawable in drawables_sprites:
            # assum that only hero is in drawable_sprites
            drawable_top = DrawableChunk(
                drawable.position.x, drawable.position.y, drawable.position.z
            )
            drawable_top.zindex = (
                sum(list(map((lambda x: x / Cube.SIZE), drawable_top.position.list())))
                + 1
            )
            drawable_top.number = 0

            drawable_bottom = DrawableChunk(
                drawable.position.x, drawable.position.y, drawable.position.z
            )
            drawable_bottom.zindex = sum(
                list(map((lambda x: x / Cube.SIZE), drawable_bottom.position.list()))
            )
            drawable_bottom.number = 1

            drawables.append(drawable_top)
            drawables.append(drawable_bottom)

            drawable_width = 32
            drawable_height = 48

            surface_tmp = pygame.Surface(
                (drawable_width, drawable_height), pygame.SRCALPHA
            )
            drawable.draw(0, 0, surface_tmp)

        for cube in self.cubes:
            drawables.append(cube)

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

                z_shift = (drawable_height // 2) * drawable.number
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
                    (0, z_shift, drawable_width, drawable_height // 2),
                )
