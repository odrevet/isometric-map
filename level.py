import pygame
from pygame.locals import *
import csv

from cube import Cube
from const import *
from point3d import Point3d
from utils import *
from drawable_chunk import DrawableChunk
from hero import Hero


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
                    # Caution: cube positions are indexes !
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
        for i in range(len(self.cubes)):
            cube = self.cubes[i]
            if cube.position.x == x and cube.position.y == y and cube.position.z == z:
                return cube

    def get_cube_index(self, x, y, z):
        for i in range(len(self.cubes)):
            cube = self.cubes[i]
            if cube.position.x == x and cube.position.y == y and cube.position.z == z:
                return i

    def draw(self, drawables_sprites, camera, surface_display):
        drawables = self.cubes.copy()

        # Work In Progress: split drawables into chunks when needed
        for drawable in drawables_sprites:
            if isinstance(drawable, Hero):
                # assum that only hero needs chunk display
                # draw in a temporary surface
                surface_tmp = pygame.Surface(
                    (drawable.drawable_width, drawable.drawable_height), pygame.SRCALPHA
                )
                drawable.draw(0, 0, surface_tmp)

                # assum 2 chunks
                nb_chunk = 2  # drawable_height // Cube.SIZE
                for number in range(nb_chunk):
                    drawable_chunk = DrawableChunk(
                        drawable.position.x,
                        drawable.position.y,
                        drawable.position.z,
                    )

                    drawable_chunk.zindex += number
                    drawable_chunk.number = nb_chunk - number - 1
                    drawable_chunk.surface = surface_tmp
                    drawable_chunk.size = Point2d(
                        drawable.drawable_width, drawable.drawable_height
                    )
                    drawables.append(drawable_chunk)
            else:
                drawables.append(drawable)

        for drawable in sorted(drawables, key=lambda drawable: drawable.zindex):
            if isinstance(drawable, Cube):
                x = (
                    camera.x
                    + drawable.position.x * Cube.SIZE
                    - drawable.position.y * Cube.SIZE
                    - Cube.SIZE
                )
                y = (
                    camera.y
                    + drawable.position.x * TILE_SIZE
                    + drawable.position.y * TILE_SIZE
                    - (Cube.SIZE * drawable.position.z)
                )
                drawable.draw(x, y, surface_display, self.image_tileset)
            else:
                drawable_iso = cartesian_to_isometric(
                    (drawable.position.x, drawable.position.y)
                )
                x = camera.x + drawable_iso.x - Cube.SIZE
                y = camera.y + drawable_iso.y - drawable.position.z - Cube.SIZE
                drawable.draw(x, y, surface_display)
