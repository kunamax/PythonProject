
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
    def __floordiv__(self, other):
        return Vector2d((self.x//other)*other,(self.y//other)*other)

    def __mod__(self, other):
        return Vector2d(self.x%other,self.y%other)
    def __str__(self):
        return f"({self.x},{self.y})"

    def precedes(self, other):
        return self.x >= other.x and self.y >= other.y

    def follows(self, other):
        return self.x <= other.x and self.y <= other.y
    def to_string(self):
        return f"({self.x},{self.y})"
    def __hash__(self):
        return hash((self.x, self.y))