import pygame

from utils import cartesian_to_isometric
from const import *
from drawable import Drawable
from cube import Cube


class Cursor(Drawable):
    def __init__(self, x=0, y=0, z=0):
        Drawable.__init__(self, x, y, z)

    def draw(self, surface_screen, camera):
        bl = cartesian_to_isometric(
            (self.position.x * Cube.SIZE, self.position.y * Cube.SIZE + Cube.SIZE)
        )
        br = cartesian_to_isometric(
            (
                self.position.x * Cube.SIZE + Cube.SIZE,
                self.position.y * Cube.SIZE + Cube.SIZE - 1,
            )
        )
        tl = cartesian_to_isometric(
            (self.position.x * Cube.SIZE, self.position.y * Cube.SIZE)
        )
        tr = cartesian_to_isometric(
            (self.position.x * Cube.SIZE + Cube.SIZE, self.position.y * Cube.SIZE - 1)
        )

        points = [
            (bl.x + camera.x, bl.y + camera.y - self.position.z * Cube.SIZE),
            (br.x + camera.x, br.y + camera.y - self.position.z * Cube.SIZE),
            (tr.x + camera.x, tr.y + camera.y - self.position.z * Cube.SIZE),
            (tl.x + camera.x, tl.y + camera.y - self.position.z * Cube.SIZE),
        ]

        pygame.draw.lines(
            surface_screen,
            (255, 255, 255),
            True,
            points,
        )

        points = [
            (
                bl.x + camera.x,
                bl.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
            (
                br.x + camera.x,
                br.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
            (
                tr.x + camera.x,
                tr.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
            (
                tl.x + camera.x,
                tl.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
        ]

        pygame.draw.lines(
            surface_screen,
            (255, 255, 255),
            True,
            points,
        )

        pygame.draw.line(
            surface_screen,
            (255, 255, 255),
            (
                tl.x + camera.x,
                tl.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
            (tl.x + camera.x, tl.y + camera.y - self.position.z * Cube.SIZE),
        )

        pygame.draw.line(
            surface_screen,
            (255, 255, 255),
            (
                bl.x + camera.x,
                bl.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
            (bl.x + camera.x, bl.y + camera.y - self.position.z * Cube.SIZE),
        )

        pygame.draw.line(
            surface_screen,
            (255, 255, 255),
            (
                tr.x + camera.x,
                tr.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
            (tr.x + camera.x, tr.y + camera.y - self.position.z * Cube.SIZE),
        )

        pygame.draw.line(
            surface_screen,
            (255, 255, 255),
            (
                br.x + camera.x,
                br.y + camera.y - self.position.z * Cube.SIZE + Cube.SIZE,
            ),
            (br.x + camera.x, br.y + camera.y - self.position.z * Cube.SIZE),
        )
