from ._tile import Tile
from ._cell import Cell
from ._wall import Wall, WallType
from .Entities.Items.Utility import Directions, Vector2d


class MapMaker():
    def __init__(self):
        self.walls_dict = {
            # EMPTY = 0
            "_": Wall(WallType(0), Directions(0)),
            # FULL = 1
            "X": Wall(WallType(1), Directions(0)),
            # HALF = 2
            "1": Wall(WallType(2), Directions(1)),
            "3": Wall(WallType(2), Directions(3)),
            "5": Wall(WallType(2), Directions(5)),
            "7": Wall(WallType(2), Directions(7)),
            # STAIRS = 3
            "0": Wall(WallType(3), Directions(0)),
            "2": Wall(WallType(3), Directions(2)),
            "4": Wall(WallType(3), Directions(4)),
            "6": Wall(WallType(2), Directions(6))
        }
        self.str_cells_dict = {
            "1111": ["XX3___7XXX",
                     "X3___7XXXX",
                     "3___7XXXXX",
                     "___7XXXXX3",
                     "__7XXXXX3_",
                     "_7XXXXX3__",
                     "7XXXXX3___",
                     "XXXXX3___7",
                     "XXXX3___7X",
                     "XXX3___7XX"],

            "0001": ["5XX____XX3",
                     "_5X___7X3_",
                     "__51__X3__",
                     "___5173___",
                     "____XX____",
                     "___7X3____",
                     "___XX_____",
                     "__7XX1____",
                     "__5XX3____",
                     "__________"],

            "0011": ["1_________",
                     "X_________",
                     "3_________",
                     "__________",
                     "__7XXX____",
                     "_7XXXX____",
                     "7XXXXX____",
                     "XXXXX3____",
                     "XXXX3_____",
                     "XXX3___7X1"],

            "0101": ["1________7",
                     "X________X",
                     "3________5",
                     "____1_____",
                     "___73_____",
                     "___5171___",
                     "____53____",
                     "1________7",
                     "X________X",
                     "3________5", ],

            "0111": ["XX3____5XX",
                     "X3_____7XX",
                     "3______X35",
                     "__7____X__",
                     "_7X3___X__",
                     "__3__7XX__",
                     "_____XXX__",
                     "1____5X3_7",
                     "x________X",
                     "3________5"],
            #################
            "": ["",
                 "",
                 "",
                 "",
                 "",
                 "",
                 "",
                 "",
                 "",
                 ""],
        }

    def create_tile(self, data: list[str]) -> Tile:
        ...

    def create_cell(self, cell_str: str) -> Cell:
        return Cell(self.walls_dict[cell_str], [])

    def __rotate_left(self, tile: Tile) -> Tile:
        new_cells = {}
        for key in tile.cells_dict.keys():
            new_cells[key] = tile.cells_dict[Vector2d(9 - key.y, key.x)]
            if new_cells[key].wall.type == WallType.HALF or new_cells[key].wall.type == WallType.STAIRS:
                new_cells[key].wall.facing = (int(new_cells[key].wall.facing) - 2) % 8
        tile.cells_dict = new_cells

        tmp = tile.upper_id
        tile.upper_id = tile.right_id
        tile.right_id = tile.lower_id
        tile.lower_id = tile.left_id
        tile.left_id = tmp
        return tile

    def __horizontal_flip(self, tile: Tile) -> Tile:
        new_cells = {}
        for key in tile.cells_dict.keys():
            new_cells[key] = tile.cells_dict[Vector2d(-key.x, key.y)]
            if new_cells[key].wall.type == WallType.HALF or new_cells[key].wall.type == WallType.STAIRS:
                new_cells[key].wall.facing = (-int(new_cells[key].wall.facing)) % 8
        tile.cells_dict = new_cells

        tmp = tile.right_id
        tile.right_id = tile.left_id
        tile.left_id = tmp
        return tile
