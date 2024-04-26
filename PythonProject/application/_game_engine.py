from map import Map, Tile

class GameEngine:
    def __init__(self):
        self.map = None

    def create_map(self):
        tiles_dictionary = {}
        lower_left_vector2d = (0, 0)
        self.map = Map(tiles_dictionary, lower_left_vector2d)

        for i in range(10):
            for j in range(10):
                cells_dict = {}
                lower_left_vector2d = (i * 10, j * 10)
                tile = Tile(cells_dict, lower_left_vector2d, self.map)
                self.map.add_tile((i, j), tile)

    def get_map(self):
        return self.map