import pygame
from pygame.locals import *

import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox

from level import *
from const import *
from cube import Cube
from cursor import Cursor
from point2d import Point2d

# init pygame
pygame.init()
pygame.font.init()
font_size = 24
font = pygame.font.SysFont("", font_size)
bgcolor = (0, 0, 0)
resolution_window = Point2d(640, 480)
resolution_screen = Point2d(320, 240)
surface_window = pygame.display.set_mode(resolution_window.list())
surface_screen = pygame.Surface(resolution_screen.list())
pygame.display.set_caption("Isometric Map Editor")
camera = Point2d(resolution_screen.x / 2, resolution_screen.y / 2)
clock = pygame.time.Clock()

# init GUI
ui_manager = pygame_gui.UIManager(resolution_screen.list(), "data/themes/classic.json")
debug_textbox = UITextBox(
    "test",
    pygame.Rect((0, 0), (resolution_screen.x, resolution_screen.y // 3)),
    manager=ui_manager,
    object_id="#toolbar_textbox",
)

# init level
level = Level()
level.read("data/level.map")

# init cursor
cursor = Cursor()
move_z = False

while True:
    time_delta = clock.tick(60) / 1000.0

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

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
            if event.key == pygame.K_RETURN:
                if (
                    cursor.position.x < 0
                    or cursor.position.y < 0
                    or cursor.position.z < 0
                    or cursor.position.x > level.size.x
                    or cursor.position.y > level.size.y
                    or cursor.position.z > level.size.z
                ):
                    print("out of bound")
                else:
                    # create a new cube
                    coords = [
                        [0, 0],
                        [0, 2],
                        [6, 2],
                    ]
                    cube = Cube(coords)
                    cube.position = Point3d(
                        cursor.position.x, cursor.position.y, cursor.position.z
                    )

                    # assign new cube to level
                    cube_index = level.get_cube_index(
                        cursor.position.x // Cube.SIZE,
                        cursor.position.y // Cube.SIZE,
                        cursor.position.z // Cube.SIZE,
                    )
                    if cube_index is None:
                        level.cubes[cube_index] = cube
                    else:
                        print(cube_index)

        elif event.type == pygame.KEYUP:
            if event.key in (K_LSHIFT, K_RSHIFT):
                move_z = False

    # Draw
    surface_screen.fill(bgcolor)
    level.draw([], camera, surface_screen)
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
    debug_text = f"Level size {level.size.x}:{level.size.y}:{level.size.z} <br/>"
    debug_text += f"Cursor {cursor.position.x}:{cursor.position.y}:{cursor.position.z}<br/>{level.get_cube(cursor.position.x,cursor.position.y,cursor.position.z)}"
    debug_textbox.html_text = debug_text
    debug_textbox.rebuild()
    ui_manager.draw_ui(surface_screen)
    ui_manager.update(time_delta)

    scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
    surface_window.blit(scaled_win, (0, 0))
    pygame.display.update()
