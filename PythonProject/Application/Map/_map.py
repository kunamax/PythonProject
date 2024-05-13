from Utility import Vector2d
from Utility import Directions
from ._tile import Tile
from ._cell import Cell
from ._wall import Wall, WallType
import random


class Map:
    def __init__(self, tiles_dictionary: dict[Vector2d, Tile]=None):
        self.tiles_dictionary = tiles_dictionary
        if self.tiles_dictionary==None:
            self.tiles_dictionary={}

    def __getitem__(self, item: Vector2d) -> Cell:
        return self.tiles_dictionary[Vector2d(item.x // 10, item.y // 10)].cells_dict[Vector2d(item.x % 10, item.y % 10)]

    def move(self):
        ...

    def generate_demo(self):
        size = 2

        for x in range(-size, size + 1):
            for y in range(-size, size + 1):
                tile = Tile(Vector2d(x, y), {})
                for i in range(10):
                    for j in range(10):
                        if random.choices([True, False], [0.3, 0.7])[0]:
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(1), Directions(0)), [])
                        else:
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(0), Directions(0)), [])
                self.tiles_dictionary[Vector2d(x, y)] = tile




        # self.tiles_dictionary[Vector2d(0, 0)].generate_demo_cross()
        #
        # self.tiles_dictionary[Vector2d(10, 0)].generate_demo_turn()
        # self.tiles_dictionary[Vector2d(0, 10)].generate_demo_turn()
        # self.tiles_dictionary[Vector2d(10, 10)].generate_demo_blank()
        #
        # self.tiles_dictionary[Vector2d(-10, 0)].generate_demo_cross()
        # self.tiles_dictionary[Vector2d(0, -10)].generate_demo_cross()
        # self.tiles_dictionary[Vector2d(-10, -10)].generate_demo_blank()
        #
        # self.tiles_dictionary[Vector2d(-10, 10)].generate_demo_cross()
        # self.tiles_dictionary[Vector2d(10, -10)].generate_demo_cross()


if __name__ == "__main__":
    size = 10
    ma = Map()
    ma.generate_demo()
    vec = Vector2d(11, -1)

    print(vec // 10)
    print(vec % 10)

    print(ma[vec].wall.type, ma[vec].wall.facing)
    print(ma.tiles_dictionary[vec // 10].lower_left_vector2d)
