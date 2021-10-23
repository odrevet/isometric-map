from copy import copy

import pygame
from pygame.math import Vector2, Vector3
from pygame.locals import *

import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox

from utils import *
from cube import Cube
from hero import Direction
from gold import Gold
from chest import Chest
from box import Box
from direction import Direction

from levels.lv import *


class Game:
    def __init__(self) -> None:
        self.level = None
        self.hero = None
        self.ui_manager = None
        self.clock = pygame.time.Clock()
        self.resolution_screen = (320, 240)
        self.resolution_window = (640, 480)
        self.surface_window = pygame.display.set_mode(self.resolution_window)
        self.surface_screen = pygame.Surface(self.resolution_screen)
        self.camera = Vector2(0, 0)

        # init GUI
        self.ui_manager = pygame_gui.UIManager(
            self.resolution_screen, "data/themes/classic.json"
        )

        self.hud_textbox = UITextBox(
            "",
            pygame.Rect((0, 0), (320, 35)),
            manager=self.ui_manager,
            object_id="#hud_textbox",
        )

        self.msg_textbox = UITextBox(
            "",
            pygame.Rect((0, 180), (320, 60)),
            manager=self.ui_manager,
            object_id="#msg_textbox",
        )
        self.msg_textbox.hide()

        if __debug__:
            self.debug_textbox = UITextBox(
                "",
                pygame.Rect((0, 35), (320, 35)),
                manager=self.ui_manager,
                object_id="#debug_textbox",
            )

    def draw(self):
        # draw
        self.surface_screen.fill((0, 0, 0))
        self.level.draw(self.camera, self.surface_screen)

        hud_text = f"{self.hero.gold}G"
        self.hud_textbox.html_text = hud_text
        self.hud_textbox.rebuild()

        # debug
        if __debug__:
            debug_text = f"{self.level.size} {self.hero.position} | {int(self.clock.get_fps())} fps"
            self.debug_textbox.html_text = debug_text
            self.debug_textbox.rebuild()

            # draw lines around drawables
            for drawable in self.level.drawables:
                bl, br, tl, tr = list(
                    map(
                        (lambda coord: cartesian_to_isometric(coord)),
                        drawable.get_coords(),
                    )
                )

                # adjust all points with camera and z position
                points = list(
                    map(
                        (
                            lambda point: (
                                point.x + self.camera.x,
                                point.y
                                + self.camera.y
                                - drawable.position.z
                                + Cube.SIZE,
                            )
                        ),
                        [bl, br, br, tr, tl, tr, tl, bl],
                    )
                )

                pygame.draw.lines(
                    self.surface_screen,
                    (255, 255, 255),
                    False,
                    points,
                )

                # Top
                points = list(
                    map(
                        (
                            lambda point: (
                                point.x + self.camera.x,
                                point.y
                                + self.camera.y
                                - drawable.position.z
                                - drawable.size.z
                                + Cube.SIZE,
                            )
                        ),
                        [bl, br, br, tr, tl, tr, tl, bl],
                    )
                )

                pygame.draw.lines(
                    self.surface_screen,
                    (255, 255, 255),
                    False,
                    points,
                )

        self.ui_manager.draw_ui(self.surface_screen)

    def update_display(self):
        scaled_win = pygame.transform.scale(
            self.surface_screen, self.surface_window.get_size()
        )
        self.surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()

    def hero_on_ground(self):
        [bl, br, tl, tr] = self.hero.get_coords()
        return not (
            self.not_solid(self.get_at(bl.x, bl.y, (self.hero.position.z - 1)))
            and self.not_solid(self.get_at(br.x, br.y, (self.hero.position.z - 1)))
            and self.not_solid(self.get_at(tl.x, tl.y, (self.hero.position.z - 1)))
            and self.not_solid(self.get_at(tr.x, tr.y, (self.hero.position.z - 1)))
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
                        self.level.cubes + self.level.drawables,
                        key=lambda drawable: drawable.zindex,
                    )
                    for drawable in sorted_drawables:
                        print(drawable)

                if event.key == pygame.K_SPACE:
                    if self.hero.on_ground:
                        self.hero.jump = True

                # action button
                if event.key == pygame.K_RETURN:
                    # interact in front of hero
                    x = self.hero.position.x
                    y = self.hero.position.y
                    z = self.hero.position.z
                    #
                    if self.hero.direction == Direction.UP:
                        y -= 8
                    elif self.hero.direction == Direction.RIGHT:
                        x += 24
                    elif self.hero.direction == Direction.DOWN:
                        y += 24
                    elif self.hero.direction == Direction.LEFT:
                        x -= 8

                    box = Box(Vector3(x, y, z), Vector3(8, 8, 8))
                    for drawable in self.level.drawables:
                        if __debug__:
                            print(f"check interact with {drawable}")
                        if box.intersect(drawable):
                            if isinstance(drawable, Chest) and not drawable.is_open:
                                drawable.open()
                            elif (
                                isinstance(drawable, NPC)
                                and drawable.on_interact is not None
                            ):
                                if self.hero.direction == Direction.LEFT:
                                    drawable.direction = Direction.RIGHT
                                elif self.hero.direction == Direction.UP:
                                    drawable.direction = Direction.DOWN
                                elif self.hero.direction == Direction.RIGHT:
                                    drawable.direction = Direction.LEFT
                                elif self.hero.direction == Direction.DOWN:
                                    drawable.direction = Direction.UP
                                drawable.on_interact()

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

        for drawable in self.level.drawables:
            if drawable.intersect_Vector3(Vector3(x, y, z)):
                return drawable

        return None

    def not_solid(self, drawable):
        return drawable is None or (drawable is not None and drawable.solid == False)

    def update_camera(self):
        self.camera = cartesian_to_isometric(
            (self.hero.position.x, self.hero.position.y)
        )
        self.camera.x = self.resolution_screen[0] // 2 - self.camera.x
        self.camera.y = (
            self.resolution_screen[1] // 2 - self.camera.y + self.hero.position.z
        )

    def update(self):
        time_delta = self.clock.tick(60) / 1000.0

        self.hero.on_ground = self.hero_on_ground()

        for drawable in self.level.drawables:
            drawable.update_zindex()

        self.events()

        # check collectibles
        drawable_index = 0
        for drawable in self.level.drawables:
            if self.hero == drawable:
                continue

            if self.hero.intersect(drawable):
                if isinstance(drawable, Gold):
                    self.hero.gold += drawable.amount
                    del self.level.drawables[drawable_index]

            drawable_index += 1

        # check events
        event_index = 0
        for event in self.level.events:
            if self.hero.intersect(event):
                event.on_intersect()

            event_index += 1

        # update hero location
        if self.hero.is_moving:
            next_pos = copy(self.hero.position)

            if self.hero.direction == Direction.UP:
                next_pos.y -= 1

                if next_pos.y >= 0:
                    at_top_left = self.get_at(next_pos.x, next_pos.y, next_pos.z)
                    at_top_right = self.get_at(
                        next_pos.x + self.hero.size.x, next_pos.y, next_pos.z
                    )

                    if self.not_solid(at_top_left) and self.not_solid(at_top_right):
                        self.hero.position = copy(next_pos)
                        self.update_camera()

            elif self.hero.direction == Direction.RIGHT:
                next_pos.x += 1

                if next_pos.x + self.hero.size.x < self.level.size.x * Cube.SIZE:
                    at_top_right = self.get_at(
                        next_pos.x + self.hero.size.x, next_pos.y, next_pos.z
                    )
                    at_btm_right = self.get_at(
                        next_pos.x + self.hero.size.x,
                        next_pos.y + self.hero.size.y,
                        next_pos.z,
                    )

                    if self.not_solid(at_top_right) and self.not_solid(at_btm_right):
                        self.hero.position = copy(next_pos)
                        self.update_camera()

            elif self.hero.direction == Direction.DOWN:
                next_pos.y += 1

                if next_pos.y + self.hero.size.y < self.level.size.y * Cube.SIZE:
                    at_btm_left = self.get_at(
                        next_pos.x, next_pos.y + self.hero.size.y, next_pos.z
                    )
                    at_btm_right = self.get_at(
                        next_pos.x + self.hero.size.x,
                        next_pos.y + self.hero.size.y,
                        next_pos.z,
                    )

                    if self.not_solid(at_btm_left) and self.not_solid(at_btm_right):
                        self.hero.position = copy(next_pos)
                        self.update_camera()

            elif self.hero.direction == Direction.LEFT:
                next_pos.x -= 1

                if next_pos.x > 0:
                    at_top_left = self.get_at(next_pos.x, next_pos.y, next_pos.z)
                    at_btm_left = self.get_at(
                        next_pos.x,
                        next_pos.y + self.hero.size.y,
                        next_pos.z,
                    )

                    if self.not_solid(at_top_left) and self.not_solid(at_btm_left):
                        self.hero.position = copy(next_pos)
                        self.update_camera()

        # jump
        if self.hero.jump == True:
            if self.hero.jump_cur >= self.hero.jump_max:
                self.hero.jump = False
                self.hero.jump_cur = 0
            else:
                self.hero.position.z += 1
                self.hero.jump_cur += 1
            self.update_camera()

        # gravity
        if self.hero.jump == False and not self.hero.on_ground:
            self.hero.position.z -= 1
            self.update_camera()

        self.ui_manager.update(time_delta)
