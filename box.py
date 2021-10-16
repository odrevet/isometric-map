class Box():
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def intersect(self, other):
        return (
            self.position.y + self.size.y > other.position.y
            and self.position.y < other.position.y + other.size.y
            and self.position.x + self.size.x > other.position.x
            and self.position.x < other.position.x + other.size.x
            and self.position.z + self.size.z > other.position.z
            and self.position.z < other.position.z + other.size.z
        )
