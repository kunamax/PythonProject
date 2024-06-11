import copy
import random

from .Entities.Items import ShopItem, Weapon, HealingPotion, Armor
from ._tile import Tile
from ._cell import Cell
from ._wall import Wall, WallType
from ._map import Map
from .Entities.Items.Utility import Directions, Vector2d


class MapMaker():
    def __init__(self):
        self.junction_chances = ["0", "0", "0", "1", "1", "2"]
        self.walls_dict = {
            # EMPTY = 0
            "_": Wall(WallType(0), Directions(0)),
            # FULL = 1
            "X": Wall(WallType(1), Directions(0)),
            # HALF = 2
            "1": Wall(WallType(2), Directions(5)),
            "3": Wall(WallType(2), Directions(3)),
            "5": Wall(WallType(2), Directions(1)),
            "7": Wall(WallType(2), Directions(7))
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

            "1101": ["XX3____5XX",
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
            "2222": ["XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX",
                     "XXXXXXXXXX"],
            # 0,2
            "0222": ["1________7",
                     "X_______7X",
                     "X1______XX",
                     "XX_____7XX",
                     "XX1____XXX",
                     "XXX___7XXX",
                     "XXX1__XXXX",
                     "XXXX_7XXXX",
                     "XXXX1XXXXX",
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
                     "3________5"],
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
                     "___7XX1___",
                     "___XXXX___",
                     "___XXXX___",
                     "___5XX3___",
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
                     "X__53_____",
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
                     "__5X3__XXX",
                     "______7XXX",
                     "_____73_XX",
                     "7X1_7X1_5X",
                     "XXX_XXX_7X",
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
                     "X3__5XX__X",
                     "X_______7X",
                     "X1______XX",
                     "X3______5X",
                     "3________5"]
        }
        keys = copy.deepcopy(self.str_cells_dict)
        for key in keys:

            # right
            new_key, new_str = self.right_rotation(key)
            self.str_cells_dict[new_key] = new_str
            
            # right
            new_key, new_str = self.right_rotation(new_key)
            self.str_cells_dict[new_key] = new_str
            

            # right
            new_key, new_str = self.right_rotation(new_key)
            self.str_cells_dict[new_key] = new_str
            

            # horizontal
            new_key, new_str = self.horizontal_rotation(new_key)
            self.str_cells_dict[new_key] = new_str
            

            # right
            new_key, new_str = self.right_rotation(new_key)
            self.str_cells_dict[new_key] = new_str
            

            # right
            new_key, new_str = self.right_rotation(new_key)
            self.str_cells_dict[new_key] = new_str
            

            # right
            new_key, new_str = self.right_rotation(new_key)
            self.str_cells_dict[new_key] = new_str
            

        self.str_cells_dict["mid shop"] = ["XXX____XXX",
                                           "XXX____XXX",
                                           "XX3____5XX",
                                           "__________",
                                           "__________",
                                           "__________",
                                           "__________",
                                           "XX1____7XX",
                                           "XXX____XXX",
                                           "XXX____XXX"]
        self.str_cells_dict["end"] = ["XXX____XXX",
                                      "XXX____XXX",
                                      "XX3____XXX",
                                      "___7X1_XXX",
                                      "___X_5_XXX",
                                      "___51_7XXX",
                                      "_____7XXXX",
                                      "XXXXXXXXXX",
                                      "XXXXXXXXXX",
                                      "XXXXXXXXXX"]

    def create_map(self, size) -> Map:
        junction_arr = [[] for _ in range(size * 2 + 1)]
        for x in range(len(junction_arr)):
            junction_arr[x] = ["?" for _ in range(size + (x % 2))]
        for x in range(size):
            for y in range(size + 1):
                if y == 0 or y == size:
                    junction_arr[x * 2 + 1][y] = "2"
                else:
                    index = random.randint(0, len(self.junction_chances) - 1)
                    random_junction = f"{self.junction_chances[index]}"
                    junction_arr[x * 2 + 1][y] = random_junction

        for x in range(size + 1):
            for y in range(size):
                index = random.randint(0, len(self.junction_chances) - 1)
                random_junction = f"{self.junction_chances[index]}"
                junction_arr[x * 2][y] = random_junction
            # print(f"{x, y}")
            # for lane in junction_arr:
            #     print(lane)
        junction_arr[0] = ["2" for i in range(size)]
        junction_arr[size * 2] = ["2" for i in range(size)]
        # starting position
        junction = random.randint(0, 1)
        junction_arr[1][1] = f"{junction}"
        junction_arr[2][0] = f"{1 - junction}"
        dim_1= len(junction_arr)
        dim_2= len(junction_arr[0])
        junction_arr[dim_1-3][dim_2-1]="1"
        junction_arr[dim_1-2][dim_2-1]="1"


        str_arr = [[copy.deepcopy("?") for _ in range(size)] for _ in range(size)]
        for x in range(size):
            for y in range(size):
                str_arr[x][y] = junction_arr[x * 2][y] + junction_arr[x * 2 + 1][y + 1] + \
                                junction_arr[(x + 1) * 2][y] + junction_arr[x * 2 + 1][y]
                # str_arr[x][y]="2021"
        str_arr[size-1][size-1]="end"
        # for lane in str_arr:
        #     print(lane)
        # print()
        map = Map()
        for x in range(size):
            for y in range(size):
                map.tiles_dictionary[Vector2d(y, x)] = self.create_tile(str_arr[y][x], Vector2d(y,x))

        return map

    def create_shop(self, first_shop: bool = True) -> Map:
        attacks = [Vector2d(x, y) for x, y in
                   [(-4, -3), (-3, -2), (-2, -2), (-1, -1), (4, -3), (3, -2), (2, -2), (1, -1)]]
        a_s = ShopItem(Weapon("Alpollo shoes", "Shoes of ghostly speed", 7, 5, copy.deepcopy(attacks)), 15)
        attacks = [Vector2d(x, y) for x, y in
                   [(1, 1), (2, 2), (3, 3), (4, 4), (2, 4), (4, 2), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-2, 4),
                    (-4, 2)]]
        i_w = ShopItem(Weapon("Ice wand", "Chilly stick of frost", 7, 2, copy.deepcopy(attacks)), 15)
        attacks = [Vector2d(x, y) for x, y in
                   [(0, 3), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (1, 3), (1, 4), (2, 5), (-1, 2), (-2, 3), (-3, 4),
                    (-4, 5), (-1, 3), (-1, 4), (-2, 5)]]
        f_s = ShopItem(Weapon("Fire staff", "Burning rod of fury", 7, 2, copy.deepcopy(attacks)), 15)
        attacks = [Vector2d(x, y) for x, y in
                   [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 4), (1, 5), (2, 5), (-1, 2),
                    (-1, 4), (-1, 5), (-2, 5)]]
        g_m = ShopItem(Weapon("Giant mace", "Crushing club of doom", 7, 2, copy.deepcopy(attacks)), 20)
        attacks = [Vector2d(0, y) for y in range(0, 10)]
        s_b = ShopItem(Weapon("Strong bow", "Bow of immense strength", 7, 4, copy.deepcopy(attacks)), 23)
        attacks = [Vector2d(x, y) for x, y in
                   [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 6), (-1, 2), (-1, 4), (-1, 6)]]
        m_b = ShopItem(Weapon("Magical bow", "Enchanted arrow launcher", 7, 4, copy.deepcopy(attacks)), 26)
        attacks = [Vector2d(x, y) for x, y in
                   [(0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 3), (1, 6), (1, 7), (1, 8), (2, 2), (2, 3), (2, 4),
                    (2, 7), (3, 3), (-1, 3), (-1, 6), (-1, 7), (-1, 8), (-2, 2), (-2, 3), (-2, 4), (-2, 7), (-3, 3), ]]
        t_b = ShopItem(Weapon("Throwable bombs", "Explosive hand grenades", 7, 6, copy.deepcopy(attacks)), 56)
        attacks = [Vector2d(x, y) for x, y in
                   [(0, 0), (-1, 1), (-2, 2), (-2, 3), (-3, 2), (1, 1), (1, 4), (2, 2), (2, 3), (2, 4), (2, 5), (3, 1),
                    (3, 2), (3, 4), (4, 1), (5, 1), (5, 2), (5, 3)]]
        c_a = ShopItem(Weapon("Crab arms", "Goofy pinching claws", 7, 9, copy.deepcopy(attacks)), 99)
        attacks = [Vector2d(x, 0) for x in [-4, -3, -2, -1, 1, 2, 3, 4]]
        w_l_s = ShopItem(Weapon("Weird laser sword", "Beaming blade of oddity", 7, 2, copy.deepcopy(attacks)), 1)
        attacks = [Vector2d(x, y) for x, y in
                   [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (-1, 3),
                    (-1, 4), (-1, 5), (-1, 6), (-2, 4), (-2, 5)]]
        b_a = ShopItem(Weapon("Battle axe", "Heavy war chopper", 7, 3, copy.deepcopy(attacks)), 35)
        attacks = [Vector2d(x, y) for x, y in
                   [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1), (-1, 0),
                    (-1, 1), (-1, 2), (-1, 3), (-2, 1)]]
        l_ = ShopItem(Weapon("Lance", "Knight's piercing pole", 7, 3, attacks), 55)
        list_of_weapons = [a_s, i_w, f_s, g_m, s_b, m_b, t_b, c_a, w_l_s, b_a, l_]
        random.shuffle(list_of_weapons)

        pot_0 = ShopItem(HealingPotion("Small Healing Potion", "Quick minor heal", 1, 5), 5)
        pot_1 = ShopItem(HealingPotion("Standard Healing Potion", "Moderate health boost", 1, 15), 15)
        pot_2 = ShopItem(HealingPotion("Large Healing Potion", "Significant health recovery", 1, 25), 25)
        pot_3 = ShopItem(HealingPotion("Mega Healing Potion", "Heals major injuries", 2, 50), 50)
        pot_4 = ShopItem(HealingPotion("Ultimate Healing Potion", "Complete health restore", 1, 100), 100)
        list_of_potions = [pot_0, pot_1, pot_2, pot_3, pot_4]

        armor_0 = ShopItem(Armor("Leather Armor", "Basic protection", 10, 1), 10)
        armor_1 = ShopItem(Armor("Iron Armor", "Solid defense", 15, 3), 30)
        armor_2 = ShopItem(Armor("Steel Armor", "Strong protection", 20, 5), 50)
        armor_3 = ShopItem(Armor("Mithril Armor", "Light and durable", 10, 7), 70)
        armor_4 = ShopItem(Armor("Dragon Scale Armor", "Ultimate defense", 25, 10), 100)
        lisot_of_armors = [armor_0, armor_1, armor_2, armor_3, armor_4]

        size = 3
        str_arr = [[copy.deepcopy("?") for _ in range(size)] for _ in range(size)]
        if first_shop:
            str_arr[0][0] = "2112"
            str_arr[0][1] = "2111"
            str_arr[0][2] = "2211"
            str_arr[1][0] = "1112"
            str_arr[1][1] = "mid shop"
            str_arr[1][2] = "1211"
            str_arr[2][0] = "1122"
            str_arr[2][1] = "1121"
            str_arr[2][2] = "1221"
        else:
            str_arr[0][0] = "2002"
            str_arr[1][0] = "0002"
            str_arr[2][0] = "0022"
            str_arr[0][1] = "2000"
            str_arr[1][1] = "0000"
            str_arr[2][1] = "0020"
            str_arr[0][2] = "2200"
            str_arr[1][2] = "0200"
            str_arr[2][2] = "0220"
        # for lane in str_arr:
        #     print(lane)
        # print()
        map = Map()
        shop_candidates = []
        for x in range(size):
            for y in range(size):
                map.tiles_dictionary[Vector2d(y, x)] = self.create_tile(str_arr[y][x], Vector2d(x, y))
        for x in range(size * 10):
            for y in range(size * 10):
                if map[Vector2d(x, y)].wall.type == WallType.EMPTY:
                    shop_candidates.append(map[Vector2d(x, y)])

        random.shuffle(shop_candidates)
        if first_shop:
            shop_candidates[0].shop_item = list_of_weapons[0]
            shop_candidates[1].shop_item = list_of_weapons[1]
            shop_candidates[2].shop_item = list_of_weapons[2]
            shop_candidates[3].shop_item = list_of_weapons[3]
            shop_candidates[4].shop_item = list_of_potions[0]
            shop_candidates[5].shop_item = list_of_potions[1]
            shop_candidates[6].shop_item = list_of_potions[2]
            shop_candidates[7].shop_item = lisot_of_armors[0]
            shop_candidates[8].shop_item = lisot_of_armors[1]
        else:
            shop_candidates[0].shop_item = list_of_weapons[0]
            shop_candidates[1].shop_item = list_of_weapons[1]
            shop_candidates[2].shop_item = list_of_weapons[2]
            shop_candidates[3].shop_item = list_of_weapons[3]
            shop_candidates[4].shop_item = list_of_potions[3]
            shop_candidates[5].shop_item = list_of_potions[4]
            shop_candidates[6].shop_item = lisot_of_armors[2]
            shop_candidates[7].shop_item = lisot_of_armors[3]
            shop_candidates[8].shop_item = lisot_of_armors[4]
        for x in range(size * 10):
            for y in range(size * 10):
                if map[Vector2d(x, y)].shop_item != None:
                    print(x, y, map[Vector2d(x, y)].shop_item.item.name)
        return map

    def create_boss_arena(self) -> Map:
        size = 2
        str_arr = [[copy.deepcopy("?") for _ in range(size)] for _ in range(size)]
        str_arr[0][0] = "2002"
        str_arr[1][0] = "0022"
        str_arr[0][1] = "2200"
        str_arr[1][1] = "0220"

        for lane in str_arr:
            print(lane)
        print()
        map = Map()
        for x in range(size):
            for y in range(size):
                map.tiles_dictionary[Vector2d(y, x)] = self.create_tile(str_arr[y][x], Vector2d(x, y))
        return map

    def create_tile(self, id: str, vector: Vector2d) -> Tile:
        # print(f"creating tile, id:{id}, v:{vector}")
        tile = Tile(vector, {})
        str_tile = self.str_cells_dict[id]
        for x in range(10):
            for y in range(10):
                tile.cells_dict[Vector2d(y, x)] = copy.deepcopy(Cell(self.walls_dict[str_tile[y][x]], []))

        return copy.deepcopy(tile)

    def right_rotation(self, key: str):
        new_key = key[-1] + key[:-1]
        new_str = [[copy.deepcopy("?") for _ in range(10)] for _ in range(10)]

        for x in range(10):
            for y in range(10):
                char = self.str_cells_dict[key][x][y]
                if char == 'x':
                    print(key)
                if char != 'X' and char != '_':
                    char = f"{(int(char) + 2) % 8}"
                new_str[y][9 - x] = char

        for x in range(10):
            s = ""
            for y in range(10):
                s += new_str[x][y]
            new_str[x] = s
        return new_key, new_str

    def horizontal_rotation(self, key: str):
        new_key = key[0] + key[3] + key[2] + key[1]
        new_str = [[copy.deepcopy("?") for _ in range(10)] for _ in range(10)]

        for x in range(10):
            for y in range(10):
                char = self.str_cells_dict[key][x][y]
                if char != 'X' and char != '_':
                    char = f"{(-int(char)) % 8}"
                new_str[x][(-y - 1) % 10] = char

        for x in range(10):
            s = ""
            for y in range(10):
                s += new_str[x][y]
            new_str[x] = s
        return new_key, new_str
