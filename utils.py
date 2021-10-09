from pygame.math import Vector2


def cartesian_to_isometric(coord):
    return Vector2(coord[0] - coord[1], (coord[0] + coord[1]) // 2)


def to_2d_coords(index, width):
    return Vector2(index % width, index // width)
