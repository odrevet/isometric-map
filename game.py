import math

import pygame
from pygame import draw
from pygame.locals import *

from utils import *
from cube import Cube
from hero import Direction
from gold import Gold
from chest import Chest
from point3d import Point3d

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
            debug_text = f"{self.level.size.x}:{self.level.size.y}:{self.level.size.z} {self.hero.position.x}:{self.hero.position.y}:{self.hero.position.z}  {self.hero.gold}G"
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
            self.get_at(bl.x, bl.y, (self.hero.position.z - 1)) is not None
            or self.get_at(br.x, br.y, (self.hero.position.z - 1)) is not None
            or self.get_at(tl.x, tl.y, (self.hero.position.z - 1)) is not None
            or self.get_at(tr.x, tr.y, (self.hero.position.z - 1)) is not None
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

    def get_at(self, x, y, z):
        index_x = x // Cube.SIZE
        index_y = y // Cube.SIZE
        index_z = z // Cube.SIZE

        cube = self.level.get_cube(index_x, index_y, index_z)

        if cube is not None:
            return cube

        for drawable in self.drawables:
            if drawable.intersect_point3d(Point3d(x, y, z)):
                print(drawable)
                return drawable

        return None


    def update(self):
        time_delta = self.clock.tick(60) / 1000.0
        [bl, br, tl, tr] = self.hero.get_coords()
        self.hero.on_ground = self.hero_on_ground([bl, br, tl, tr])

        for drawable in self.drawables:
            drawable.update_zindex()

        self.events()

        # check collectible
        drawable_index = 0
        for drawable in self.drawables:
            if self.hero == drawable:
                continue

            if self.hero.intersect(drawable):
                if isinstance(drawable, Gold):
                    self.hero.gold += 5
                    del self.drawables[drawable_index]

            drawable_index += 1

        # update hero location
        if self.hero.is_moving:
            if self.hero.direction == Direction.UP:
                if (
                    self.hero.position.y - 1 >= 0
                    and self.get_at(tl.x, (tl.y - 1), self.hero.position.z) is None
                    and self.get_at(tr.x, (tr.y - 1), self.hero.position.z) is None
                ):
                    self.hero.position.y -= 1
            elif self.hero.direction == Direction.RIGHT:
                if (
                    math.ceil((self.hero.position.x + 1) / (Cube.SIZE))
                    < self.level.size.x
                    and self.get_at((tr.x + 1), tr.y, self.hero.position.z) is None
                    and self.get_at((br.x + 1), br.y, self.hero.position.z) is None
                ):
                    self.hero.position.x += 1
            elif self.hero.direction == Direction.DOWN:
                if (
                    math.ceil((self.hero.position.y + 1) / (Cube.SIZE))
                    < self.level.size.y
                    and self.get_at(bl.x, (bl.y + 1), self.hero.position.z) is None
                    and self.get_at(br.x, (br.y + 1), self.hero.position.z) is None
                ):
                    self.hero.position.y += 1
            elif self.hero.direction == Direction.LEFT:
                if (
                    self.hero.position.x - 1 >= 0
                    and self.get_at((tl.x - 1), tl.y, self.hero.position.z) is None
                    and self.get_at((bl.x - 1), bl.y, self.hero.position.z) is None
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
