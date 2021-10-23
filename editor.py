import argparse
from os.path import exists

import pygame
from pygame.math import Vector2, Vector3

import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox

from level import *
from const import *
from cube import Cube
from cursor import Cursor


def add_cube(level, cursor):
    cube_index = level.get_cube_index(
        cursor.position.x,
        cursor.position.y,
        cursor.position.z,
    )
    if cube_index is None:
        cube = Cube(
            coords=[
                Vector2(0, 0),
                Vector2(0, 2),
                Vector2(6, 2),
            ]
        )
        cube.position = Vector3(
            cursor.position.x * Cube.SIZE,
            cursor.position.y * Cube.SIZE,
            cursor.position.z * Cube.SIZE,
        )
        cube.indexes = Vector3(
            cursor.position.x,
            cursor.position.y,
            cursor.position.z,
        )
        cube.update_zindex()
        level.cubes.append(cube)


def to_1d_coords(position, width):
    return position.x + width * position.y


def save(level, filename):
    tileset_width = level.image_tileset.get_width() // TILE_SIZE
    f = open(filename, "w")
    for cube in level.cubes:
        c0 = int(to_1d_coords(cube.coords[0], tileset_width))
        c1 = int(to_1d_coords(cube.coords[1], tileset_width))
        c2 = int(to_1d_coords(cube.coords[2], tileset_width))
        f.write(
            f"{int(cube.indexes.x)}:{int(cube.indexes.y)}:{int(cube.indexes.z)} {c0}:{c1}:{c2}\n"
        )


parser = argparse.ArgumentParser()
parser.add_argument("--level", type=str, required=True)
args = vars(parser.parse_args())

# init pygame
pygame.init()
pygame.font.init()
font_size = 24
font = pygame.font.SysFont("", font_size)
bgcolor = (0, 0, 0)
resolution_window = (640, 480)
resolution_screen = (320, 240)
surface_window = pygame.display.set_mode(resolution_window)
surface_screen = pygame.Surface(resolution_screen)
pygame.display.set_caption("Isometric Map Editor")
camera = Vector2(0, 0)
clock = pygame.time.Clock()

# init GUI
ui_manager = pygame_gui.UIManager(resolution_screen, "data/themes/classic.json")
hud_textbox = UITextBox(
    "test",
    pygame.Rect((0, 0), (resolution_screen[0], resolution_screen[1] // 3)),
    manager=ui_manager,
    object_id="#toolbar_textbox",
)

# init level
level = Level()

if exists(args["level"]):
    level.read(args["level"])

# init cursor
cursor = Cursor()
move_z = False

while True:
    time_delta = clock.tick(60) / 1000.0

    # center camera on cursor
    camera = cartesian_to_isometric(
        (cursor.position.x * Cube.SIZE, cursor.position.y * Cube.SIZE)
    )
    camera.x = resolution_screen[0] // 2 - camera.x
    camera.y = resolution_screen[1] // 2 - camera.y + cursor.position.z * Cube.SIZE

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

            if event.key == pygame.K_s:
                save(level, args["level"])

            if event.key in (K_LSHIFT, K_RSHIFT):
                move_z = True

            if event.key == pygame.K_LEFT:
                cursor.position.x -= 1

            if event.key == pygame.K_RIGHT:
                cursor.position.x += 1

            if event.key == pygame.K_UP:
                if move_z == True:
                    cursor.position.z += 1
                else:
                    cursor.position.y -= 1

            if event.key == pygame.K_DOWN:
                if move_z == True:
                    cursor.position.z -= 1
                else:
                    cursor.position.y += 1

            if event.key == pygame.K_BACKSPACE:
                cube_index = level.get_cube_index(
                    cursor.position.x, cursor.position.y, cursor.position.z
                )
                if cube_index is not None:
                    del level.cubes[cube_index]
                    level.update_size()

            if event.key == pygame.K_RETURN:
                if cursor.position.x < 0:
                    x = cursor.position.x
                    for cube in level.cubes:
                        cube.position.x -= cursor.position.x * Cube.SIZE
                        cube.indexes.x -= cursor.position.x
                        cube.update_zindex()
                    cursor.position.x -= x

                if cursor.position.y < 0:
                    y = cursor.position.y
                    for cube in level.cubes:
                        cube.position.y -= cursor.position.y * Cube.SIZE
                        cube.indexes.y -= cursor.position.y
                        cube.update_zindex()
                    cursor.position.y -= y

                add_cube(level, cursor)
                level.update_size()

        elif event.type == pygame.KEYUP:
            if event.key in (K_LSHIFT, K_RSHIFT):
                move_z = False

    # Draw
    surface_screen.fill(bgcolor)
    level.draw(camera, surface_screen)
    cursor.draw(surface_screen, camera)

    # Draw level boundaries
    bl = cartesian_to_isometric((0, level.size.y * Cube.SIZE + Cube.SIZE))
    br = cartesian_to_isometric(
        (
            level.size.x * Cube.SIZE + Cube.SIZE,
            level.size.y * Cube.SIZE + Cube.SIZE,
        )
    )
    tl = cartesian_to_isometric((0, 0))
    tr = cartesian_to_isometric((level.size.x * Cube.SIZE + Cube.SIZE, 0))

    points = [
        (bl.x + camera.x, bl.y + camera.y),
        (br.x + camera.x, br.y + camera.y),
        (tr.x + camera.x, tr.y + camera.y),
        (tl.x + camera.x, tl.y + camera.y),
    ]

    pygame.draw.lines(
        surface_screen,
        (255, 255, 255),
        True,
        points,
    )

    points = [
        (bl.x + camera.x, bl.y + camera.y - level.size.y * Cube.SIZE),
        (br.x + camera.x, br.y + camera.y - level.size.y * Cube.SIZE),
        (tr.x + camera.x, tr.y + camera.y - level.size.y * Cube.SIZE),
        (tl.x + camera.x, tl.y + camera.y - level.size.y * Cube.SIZE),
    ]

    pygame.draw.lines(
        surface_screen,
        (255, 255, 255),
        True,
        points,
    )

    # Draw HUD
    hud_text = f"Level size {level.size}<br/>"
    hud_text += f"Cursor at {cursor.position}<br/>{level.get_cube(cursor.position.x,cursor.position.y,cursor.position.z)}"
    hud_textbox.html_text = hud_text
    hud_textbox.rebuild()
    ui_manager.draw_ui(surface_screen)
    ui_manager.update(time_delta)

    scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
    surface_window.blit(scaled_win, (0, 0))
    pygame.display.update()
