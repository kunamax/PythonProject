import copy
import random

from ._tile import Tile
from ._cell import Cell
from ._wall import Wall, WallType
from ._map import Map
from .Entities.Items.Utility import Directions, Vector2d


class MapMaker():
    def __init__(self):
        self.junction_chances=["0","0","0","1","1","2"]
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
            "6": Wall(WallType(3), Directions(6))
        }
        self.str_cells_dict = {
            # 0,1
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

            "1000": ["5XX____XX3",
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

            "1110": ["XX3____5XX",
                     "X3_____7XX",
                     "3______X35",
                     "__7____X__",
                     "_7X3___X__",
                     "__3__7XX__",
                     "_____XXX__",
                     "1____5X3_7",
                     "X________X",
                     "3________5"],
            # 1,2
            "1211": ["XXX____XXX",
                     "XX3____5XX",
                     "X3_7__1_5X",
                     "_________X",
                     "_________X",
                     "_________X",
                     "_________X",
                     "X1_5__3_7X",
                     "XX1____7XX",
                     "XXX____XXX"],
            "2211": ["XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "___5XXXXXX",
                     "____5XXXXX",
                     "_____5XXXX",
                     "______5XXX",
                     "X1_____XXX",
                     "XX1____XXX",
                     "XXX____XXX"],
            "1212": ["XXX____XXX",
                     "XX3____5XX",
                     "X3__71__5X",
                     "X__7XX1__X",
                     "X__XXXX__X",
                     "X__XXXX__X",
                     "X__5XX3__X",
                     "X1__53__7X",
                     "XX1____7XX",
                     "XXX____XXX"],
            "1222": ["XXX____XXX",
                     "XX3____5XX",
                     "X3__71__5X",
                     "X__7XX1__X",
                     "X__XXXX__X",
                     "X__XXXX__X",
                     "X__5XX3__X",
                     "X1__53__7X",
                     "XX1____7XX",
                     "XXXXXXXXXX"],
            "2222": ["X00000000X",
                     "6________2",
                     "6________2",
                     "6________2",
                     "6________2",
                     "6________2",
                     "6________2",
                     "6________2",
                     "6________2",
                     "X44444444X"],
            # 0,2
            "0222": ["6________2",
                     "X6______2X",
                     "XX6____2XX",
                     "XXX6__2XXX",
                     "XXXX62XXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX"],
            "0202": ["1________7",
                     "X_______7X",
                     "X1______XX",
                     "XX______5X",
                     "XX1______X",
                     "XX3______X",
                     "XX______7X",
                     "X3______XX",
                     "X_______5X",
                     "3XXXXXXXX5"],
            "2000": ["5XXXXXXXX3",
                     "____53____",
                     "__________",
                     "__________",
                     "____71____",
                     "__7XXXX1__",
                     "__XXXXXX__",
                     "__5X35X3__",
                     "__________",
                     "__________"],
            "0022": ["1_________",
                     "X_________",
                     "X1___7X1__",
                     "XX___XXX__",
                     "XX1__5X3__",
                     "XXX_______",
                     "XXX1______",
                     "XXXXX1____",
                     "XXXXXXX1__",
                     "XXXXXXXXX1"],
            "0000": ["__________",
                     "__________",
                     "__________",
                     "___74X1___",
                     "___XXX6___",
                     "___2XXX___",
                     "___5X03___",
                     "__________",
                     "__________",
                     "__________"],
            "0210": ["_________7",
                     "________7X",
                     "_______7XX",
                     "____7XXXXX",
                     "____XXX35X",
                     "____5X3__X",
                     "_________X",
                     "_________X",
                     "_________X",
                     "7X1____7XX"],
            "0112": ["1________7",
                     "X1______XX",
                     "XX1__X17XX",
                     "XXX__5XXX3",
                     "X5X1__5X3_",
                     "X_5X1_____",
                     "X__51_____",
                     "X________7",
                     "X1_______X",
                     "XX1____7XX"],
            "0221": ["1________7",
                     "X________X",
                     "X1______7X",
                     "5X1___5XXX",
                     "_5X1___5XX",
                     "________5X",
                     "_________X",
                     "1__7X1__7X",
                     "XXXXXX17XX",
                     "XXXXXXXXXX"],
            "0201": ["1________7",
                     "X17X1___7X",
                     "XXXXX__7XX",
                     "3_5X3__XXX",
                     "______7XXX",
                     "_____73_XX",
                     "7X1_7X1_5X",
                     "XXX_XXX_1X",
                     "X3__5X3_5X",
                     "3________5"],
            "0121": ["1________7",
                     "X1______7X",
                     "XX_____7XX",
                     "5X1___7XX3",
                     "_XXX______",
                     "_5X3______",
                     "____7X1___",
                     "1____XX1_7",
                     "XXX1_5XXXX",
                     "XXXXXXXXXX"],
            "1202": ["XX3___7XXX",
                     "X3____XXXX",
                     "X___XX3__X",
                     "X1__5X__7X",
                     "XX__7X1_5X",
                     "X3__3XX__X",
                     "X_______7X",
                     "X1______XX",
                     "X3______5X",
                     "3________5"],
        }
        keys=copy.deepcopy(self.str_cells_dict)
        for key in keys:
            #right
            new_key,new_str=self.right_rotation(key)
            self.str_cells_dict[new_key]=new_str
            #right
            new_key,new_str=self.right_rotation(new_key)
            self.str_cells_dict[new_key]=new_str
            #right
            new_key,new_str=self.right_rotation(new_key)
            self.str_cells_dict[new_key]=new_str
            #horizontal
            new_key,new_str=self.horizontal_rotation(new_key)
            self.str_cells_dict[new_key]=new_str
            #right
            new_key,new_str=self.right_rotation(new_key)
            self.str_cells_dict[new_key]=new_str
            #right
            new_key,new_str=self.right_rotation(new_key)
            self.str_cells_dict[new_key]=new_str
            #right
            new_key,new_str=self.right_rotation(new_key)
            self.str_cells_dict[new_key]=new_str





    def create_map(self,size)->Map:
        junction_arr=[[] for _ in range(size*2+1)]
        for x in range(len(junction_arr)):
            junction_arr[x]=["?" for i in range(size+(x%2))]
        for x in range(size):
            for y in range(size+1):
                if y == 0 or y==size:
                    junction_arr[x*2+1][y]="2"
                else:
                    index = random.randint(0, len(self.junction_chances) - 1)
                    random_junction=f"{self.junction_chances[index]}"
                    junction_arr[x*2+1][y]=random_junction

        for x in range(size+1):
            for y in range(size):
                index = random.randint(0, len(self.junction_chances) - 1)
                random_junction = f"{self.junction_chances[index]}"
                junction_arr[x*2][y] = random_junction
            # print(f"{x, y}")
            # for lane in junction_arr:
            #     print(lane)
        junction_arr[0] = ["2" for i in range(size)]
        junction_arr[size*2] = ["2" for i in range(size)]
        str_arr=[[copy.deepcopy("?") for _ in range(size)] for _ in range(size)]
        for x in range(size):
            for y in range(size):
                str_arr[x][y]=junction_arr[x*2][y]+junction_arr[x*2+1][y+1]+\
                              junction_arr[(x+1)*2][y]+junction_arr[x*2+1][y]
        for lane in str_arr:
            print(lane)
        print()
        map=Map()
        for x in range(size):
            for y in range(size):
                map.tiles_dictionary[Vector2d(x,y)]=self.create_tile(str_arr[x][y],Vector2d(x,y))
        return map
    def create_tile(self, id: str,vector:Vector2d) -> Tile:
        # print(f"creating tile, id:{id}, v:{vector}")
        tile=Tile(vector,{})
        str_tile=self.str_cells_dict[id]
        for x in range(10):
            for y in range(10):
                tile.cells_dict[Vector2d(x,y)]=Cell(self.walls_dict[str_tile[x][y]],[])

        return tile
    def create_cell(self, cell_str: str) -> Cell:
        return Cell(self.walls_dict[cell_str], [])

    def right_rotation(self, key: str):
        new_key = key[-1] + key[:-1]
        new_str = [[copy.deepcopy("?") for _ in range(10)] for _ in range(10)]

        for x in range(10):
            for y in range(10):
                char = self.str_cells_dict[key][x][y]
                if char=='x':
                    print(key)
                if char != 'X' and char != '_':
                    char = f"{(int(char)+2) % 8}"
                new_str[y][9-x] = char

        for x in range(10):
            s = ""
            for y in range(10):
                s += new_str[x][y]
            new_str[x] = s
        return new_key,new_str
    def horizontal_rotation(self, key: str):
        new_key = key[0] + key[3] + key[2] + key[1]
        new_str = [[copy.deepcopy("?") for _ in range(10)] for _ in range(10)]

        for x in range(10):
            for y in range(10):
                char = self.str_cells_dict[key][x][y]
                if char != 'X' and char != '_':
                    char = f"{(-int(char)) % 8}"
                new_str[x][(-y-1)%10] = char

        for x in range(10):
            s = ""
            for y in range(10):
                s += new_str[x][y]
            new_str[x] = s
        return new_key,new_str