from PythonProject.Utility.Vector2d import Vector2d
from PythonProject.Map.Tile import Tile
from PythonProject.Map.Cell import Cell


class Map:
    def __init__(self, tiles_dictionary: dict[Vector2d, Tile]=None):
        self.tiles_dictionary = tiles_dictionary
        if self.tiles_dictionary==None:
            self.tiles_dictionary={}

    def __getitem__(self, item: Vector2d) -> Cell:
        return self.tiles_dictionary[item // 10][item % 10]

    def generate_demo(self)->None:
        coordinates = [-10, 0, 10]
        for x in coordinates:
            for y in coordinates:
                self.tiles_dictionary[Vector2d(x, y)] = Tile(Vector2d(x, y), {})

        self.tiles_dictionary[Vector2d(0, 0)].generate_demo_cross()

        self.tiles_dictionary[Vector2d(10, 0)].generate_demo_turn()
        self.tiles_dictionary[Vector2d(0, 10)].generate_demo_turn()
        self.tiles_dictionary[Vector2d(10, 10)].generate_demo_blank()

        self.tiles_dictionary[Vector2d(-10, 0)].generate_demo_cross()
        self.tiles_dictionary[Vector2d(0, -10)].generate_demo_cross()
        self.tiles_dictionary[Vector2d(-10, -10)].generate_demo_blank()

        self.tiles_dictionary[Vector2d(-10, 10)].generate_demo_cross()
        self.tiles_dictionary[Vector2d(10, -10)].generate_demo_cross()


if __name__ == "__main__":
    size = 10
    ma = Map()
    ma.generate_demo()
    vec = Vector2d(11, -1)

    print(vec // 10)
    print(vec % 10)

    print(ma[vec].wall.type, ma[vec].wall.facing)
    print(ma.tiles_dictionary[vec // 10].lower_left_vector2d)
