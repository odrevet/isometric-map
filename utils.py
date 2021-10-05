from point2d import Point2d


def cartesian_to_isometric(coord):
    return Point2d(coord[0] - coord[1], (coord[0] + coord[1]) // 2)

def to_2d_coords(index, width):
    return Point2d(index % width, index // width)

