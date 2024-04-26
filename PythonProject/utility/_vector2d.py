from _directions import Directions
class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def precedes(self, other):
        return self.x >= other.x and self.y >= other.y

    def follows(self, other):
        return self.x <= other.x and self.y <= other.y
    def rotate_to(self,direction):
        result = {
            Directions.NORTH: self,
            Directions.EAST: Vector2d(self.y,-self.x),
            Directions.SOUTH: Vector2d(-self.x,-self.y),
            Directions.WEST: Vector2d(-self.y,self.x)
        }
        return result[direction]
    def to_string(self):
        return f"({self.x},{self.y})"
