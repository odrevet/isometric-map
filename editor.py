import pygame
from pygame.locals import *

from hero import Hero
from level import *
from const import *

pygame.init()
pygame.font.init()
font_size = 24
font = pygame.font.SysFont("", font_size)
bgcolor = (0, 0, 0)
resolution_window = (640, 480)
resolution_screen = (320, 240)
surface_window = pygame.display.set_mode(resolution_window)
surface_screen = pygame.Surface(resolution_screen)
pygame.display.set_caption("Isometric map")

level = Level()
level.read("data/level.map")

hero = Hero()
camera = [resolution_screen[0] / 2, resolution_screen[1] / 2]

coords = [0, 0, 0]  # x y z

clock = pygame.time.Clock()

while True:
    time_delta = clock.tick(60) / 1000.0
    surface_screen.fill(bgcolor)
    level.draw(hero, camera, surface_screen)

    bl = cartesian_to_isometric(
        (coords[0] * CUBE_SIZE, coords[1] * CUBE_SIZE + CUBE_SIZE)
    )
    br = cartesian_to_isometric(
        (coords[0] * CUBE_SIZE + CUBE_SIZE, coords[1] * CUBE_SIZE + CUBE_SIZE)
    )
    tl = cartesian_to_isometric((coords[0] * CUBE_SIZE, coords[1] * CUBE_SIZE))
    tr = cartesian_to_isometric(
        (coords[0] * CUBE_SIZE + CUBE_SIZE, coords[1] * CUBE_SIZE)
    )

    points = [
        (bl[0] + camera[0], bl[1] + camera[1]),
        (br[0] + camera[0], br[1] + camera[1]),
        (tr[0] + camera[0], tr[1] + camera[1]),
        (tl[0] + camera[0], tl[1] + camera[1]),
    ]

    pygame.draw.lines(
        surface_screen,
        (255, 255, 255),
        True,
        points,
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

            if event.key == pygame.K_LEFT:
                coords[0] -= 1
            if event.key == pygame.K_RIGHT:
                coords[0] += 1
            if event.key == pygame.K_UP:
                coords[1] -= 1
            if event.key == pygame.K_DOWN:
                coords[1] += 1
            if event.key == pygame.K_SPACE:
                pass

        if __debug__:
            textsurface = font.render(
                f"Level size {level.size[0]}:{level.size[1]}:{level.size[2]}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 0))

            textsurface = font.render(
                f"{coords[0]} : {coords[1]} : {coords[2]} : {level.tile(coords[0],coords[1],coords[2])}",
                False,
                (255, 255, 255),
            )
            surface_screen.blit(textsurface, (0, font_size * 1))

        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()
