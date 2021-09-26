from drawable import Drawable
from const import TILE_SIZE
from point3d import Point3d


class Cube(Drawable):
    SIZE = TILE_SIZE * 2

    def __init__(self, coords):
        super().__init__()
        self.coords = coords
        self.indexes = Point3d(0, 0, 0)

    def draw(self, x, y, surface_display, image_tileset):
        top, left, right = self.coords

        if top is not None:
            surface_display.blit(
                image_tileset,
                (x, y),
                (top.x * TILE_SIZE, top.y * TILE_SIZE, Cube.SIZE * 2, Cube.SIZE),
            )
        if left is not None:
            surface_display.blit(
                image_tileset,
                (x, y + TILE_SIZE),
                (
                    left.x * TILE_SIZE,
                    left.y * TILE_SIZE,
                    TILE_SIZE * 2,
                    TILE_SIZE * 3,
                ),
            )
        if right is not None:
            surface_display.blit(
                image_tileset,
                (x + TILE_SIZE * 2, y + TILE_SIZE),
                (
                    right.x * TILE_SIZE,
                    right.y * TILE_SIZE,
                    TILE_SIZE * 2,
                    TILE_SIZE * 3,
                ),
            )
