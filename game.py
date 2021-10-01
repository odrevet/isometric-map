import math

import pygame
from pygame.locals import *

from utils import *
from cube import Cube
from hero import Direction


class Game:
    def __init__(self) -> None:
        self.level = None
        self.drawables = []
        self.hero = None
        self.ui_manager = None
        self.clock = pygame.time.Clock()

    def add_drawable(self, drawable):
        self.drawables.append(drawable)

    def draw(self, camera, surface_screen):
        # draw
        surface_screen.fill((0, 0, 0))
        self.level.draw(self.drawables, camera, surface_screen)

        # debug
        if __debug__:
            debug_text = f"{self.level.size.x}:{self.level.size.y}:{self.level.size.z} {self.hero.position.x}:{self.hero.position.y}:{self.hero.position.z}"
            self.debug_textbox.html_text = debug_text
            self.debug_textbox.rebuild()
            self.ui_manager.draw_ui(surface_screen)

            # draw lines around hero
            # get hero coords and find isometric locations
            bl, br, tl, tr = list(
                map(
                    (lambda coord: cartesian_to_isometric(coord.list())),
                    self.hero.get_coords(),
                )
            )

            # adjust all points with camera and hero z position
            points = list(
                map(
                    (
                        lambda point: (
                            point.x + camera.x,
                            point.y + camera.y - self.hero.position.z + Cube.SIZE,
                        )
                    ),
                    [bl, br, br, tr, tl, tr, tl, bl],
                )
            )

            pygame.draw.lines(
                surface_screen,
                (255, 255, 255),
                False,
                points,
            )

    def hero_on_ground(self, coords):
        [bl, br, tl, tr] = coords
        return (
            self.level.get_cube(
                bl.x // Cube.SIZE,
                bl.y // Cube.SIZE,
                (self.hero.position.z - 1) // Cube.SIZE,
            )
            is not None
            or self.level.get_cube(
                br.x // Cube.SIZE,
                br.y // Cube.SIZE,
                (self.hero.position.z - 1) // Cube.SIZE,
            )
            is not None
            or self.level.get_cube(
                tl.x // Cube.SIZE,
                tl.y // Cube.SIZE,
                (self.hero.position.z - 1) // Cube.SIZE,
            )
            is not None
            or self.level.get_cube(
                tr.x // Cube.SIZE,
                tr.y // Cube.SIZE,
                (self.hero.position.z - 1) // Cube.SIZE,
            )
            is not None
        )

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_LEFT:
                    self.hero.is_moving = True
                    self.hero.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.hero.is_moving = True
                    self.hero.direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.hero.is_moving = True
                    self.hero.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.hero.is_moving = True
                    self.hero.direction = Direction.DOWN

                if __debug__ and event.key == pygame.K_d:
                    sorted_drawables = sorted(
                        self.level.cubes + self.drawables,
                        key=lambda drawable: drawable.zindex,
                    )
                    for drawable in sorted_drawables:
                        print(drawable)

                if event.key == pygame.K_SPACE:
                    if self.hero.on_ground:
                        self.hero.jump = True
            elif event.type == KEYUP:
                if event.key in [
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                ]:
                    self.hero.is_moving = False

    def update(self):
        time_delta = self.clock.tick(60) / 1000.0
        [bl, br, tl, tr] = self.hero.get_coords()
        self.hero.on_ground = self.hero_on_ground([bl, br, tl, tr])

        for drawable in self.drawables:
            drawable.update_zindex()

        self.events()

        # update hero location
        if self.hero.is_moving:
            if self.hero.direction == Direction.UP:
                if (
                    self.hero.position.y - 1 >= 0
                    and self.level.get_cube(
                        tl.x // Cube.SIZE,
                        (tl.y - 1) // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                    and self.level.get_cube(
                        tr.x // Cube.SIZE,
                        (tr.y - 1) // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                ):
                    self.hero.position.y -= 1
            elif self.hero.direction == Direction.RIGHT:
                if (
                    math.ceil((self.hero.position.x + 1) / (Cube.SIZE))
                    < self.level.size.x
                    and self.level.get_cube(
                        (tr.x + 1) // Cube.SIZE,
                        tr.y // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                    and self.level.get_cube(
                        (br.x + 1) // Cube.SIZE,
                        br.y // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                ):
                    self.hero.position.x += 1
            elif self.hero.direction == Direction.DOWN:
                if (
                    math.ceil((self.hero.position.y + 1) / (Cube.SIZE))
                    < self.level.size.y
                    and self.level.get_cube(
                        bl.x // Cube.SIZE,
                        (bl.y + 1) // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                    and self.level.get_cube(
                        br.x // Cube.SIZE,
                        (br.y + 1) // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                ):
                    self.hero.position.y += 1
            elif self.hero.direction == Direction.LEFT:
                if (
                    self.hero.position.x - 1 >= 0
                    and self.level.get_cube(
                        (tl.x - 1) // Cube.SIZE,
                        tl.y // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                    and self.level.get_cube(
                        (bl.x - 1) // Cube.SIZE,
                        bl.y // Cube.SIZE,
                        self.hero.position.z // Cube.SIZE,
                    )
                    is None
                ):
                    self.hero.position.x -= 1

        # jump
        if self.hero.jump == True:
            if self.hero.jump_cur >= self.hero.jump_max:
                self.hero.jump = False
                self.hero.jump_cur = 0
            else:
                self.hero.position.z += 1
                self.hero.jump_cur += 1

        # gravity
        if self.hero.jump == False and not self.hero.on_ground:
            self.hero.position.z -= 1

        self.ui_manager.update(time_delta)
