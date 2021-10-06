from parse import parse

import pygame
from pygame.locals import *

from cube import Cube
from const import *
from point3d import Point3d
from utils import *
from drawable_chunk import DrawableChunk
from hero import Hero
from level import *


class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cubes = []
        self.drawables = []
        self.image_tileset = pygame.image.load("res/tileset.png")
        self.size = Point3d()

    def add_drawable(self, drawable):
        self.drawables.append(drawable)

    def read(self, filename):
        tileset_width = self.image_tileset.get_width() // TILE_SIZE
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
            for line in lines:
                r = parse("{:d}:{:d}:{:d} {:d}:{:d}:{:d}", line)

                c0 = to_2d_coords(
                    r[3],
                    tileset_width,
                )

                c1 = to_2d_coords(
                    r[4],
                    tileset_width,
                )

                c2 = to_2d_coords(
                    r[5],
                    tileset_width,
                )

                coords = [c0, c1, c2]

                cube = Cube(coords)
                cube.position = Point3d(
                    r[0] * Cube.SIZE, r[1] * Cube.SIZE, r[2] * Cube.SIZE
                )

                cube.indexes = Point3d(r[0], r[1], r[2])
                cube.zindex = sum(cube.indexes.list())
                self.cubes.append(cube)

            self.update_size()

    def update_size(self):
        for cube in self.cubes:
            if self.size.x < cube.indexes.x + 1:
                self.size.x = cube.indexes.x + 1

            if self.size.y < cube.indexes.y + 1:
                self.size.y = cube.indexes.y + 1

            if self.size.z < cube.indexes.z + 1:
                self.size.z = cube.indexes.z + 1

    def get_cube(self, x, y, z):
        for i in range(len(self.cubes)):
            cube = self.cubes[i]
            if cube.indexes.x == x and cube.indexes.y == y and cube.indexes.z == z:
                return cube

    def get_cube_index(self, x, y, z):
        for i in range(len(self.cubes)):
            cube = self.cubes[i]
            if cube.indexes.x == x and cube.indexes.y == y and cube.indexes.z == z:
                return i

    def draw(self, camera, surface_display):
        drawables_with_chunks = []

        # Work In Progress: split drawables into chunks when needed
        for drawable in self.drawables:
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
                        drawable.position.z + 16,  # Shift
                    )

                    # TODO fix drawing when hero jump
                    drawable_chunk.zindex = (
                        sum(
                            list(
                                map(
                                    (lambda x: x / Cube.SIZE),
                                    drawable_chunk.position.list(),
                                )
                            )
                        )
                        + number
                        - 1
                    )

                    drawable_chunk.number = nb_chunk - number - 1
                    drawable_chunk.surface = surface_tmp
                    drawable_chunk.size = Point2d(
                        drawable.drawable_width, drawable.drawable_height
                    )
                    drawables_with_chunks.append(drawable_chunk)
            else:
                drawables_with_chunks.append(drawable)

        sorted_drawables = sorted(
            self.cubes + drawables_with_chunks, key=lambda drawable: drawable.zindex
        )

        for drawable in sorted_drawables:
            drawable_iso = cartesian_to_isometric(
                (drawable.position.x, drawable.position.y)
            )
            x = camera.x + drawable_iso.x - Cube.SIZE
            y = camera.y + drawable_iso.y - drawable.position.z

            if isinstance(drawable, Cube):
                drawable.draw(x, y, surface_display, self.image_tileset)
            else:
                drawable.draw(x, y, surface_display)
