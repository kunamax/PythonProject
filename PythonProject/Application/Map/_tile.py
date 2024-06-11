import random
from .Entities.Items import Armor,Weapon,HealingPotion,ShopItem
from .Entities.Items.Utility import Vector2d, Directions
from ._cell import Cell
from ._wall import Wall,WallType
class Tile:
    def __init__(self,lower_left_vector2d:Vector2d,cells_dict:dict[Vector2d,Cell]):
        self.cells_dict=cells_dict #should have 100 vectors
        self.lower_left_vector2d=lower_left_vector2d
        self.upper_id=None
        self.right_id=None
        self.lower_id=None
        self.left_id=None
    def __getitem__(self, item:Vector2d)->Cell:
        return self.cells_dict[item]

    def generate_demo_blank(self):
        size=10
        for x in range(size):
            for y in range(size):
                self.cells_dict[Vector2d(x,y)]=Cell(Wall(WallType(0),Directions(0)),[])
    def generate_demo_cross(self):
        self.generate_demo_blank()
        wall_coordinates=[0,1,2,7,8,9]
        for x in wall_coordinates:
            for y in wall_coordinates:
                self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
        self.cells_dict[Vector2d(4, 4)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(5, 4)] = Cell(Wall(WallType(2), Directions(3)), [])
        self.cells_dict[Vector2d(4, 5)] = Cell(Wall(WallType(2), Directions(7)), [])
        self.cells_dict[Vector2d(5, 5)] = Cell(Wall(WallType(2), Directions(1)), [])
    def generate_demo_turn(self,location:str):
        size = 10
        self.generate_demo_blank()
        for x in range(size):
            for y in [7,8,9]:
                self.cells_dict[Vector2d(x,y)]=Cell(Wall(WallType(1),Directions(0)),[])

        for x in [7,8,9]:
            for y in range(size):
                self.cells_dict[Vector2d(x,y)]=Cell(Wall(WallType(1),Directions(0)),[])

        for vec in [Vector2d(0,0),Vector2d(1,0),Vector2d(0,1),Vector2d(1,1),Vector2d(2,0),Vector2d(0,2),
                    Vector2d(6,6),Vector2d(6,5),Vector2d(5,6),Vector2d(5,5),Vector2d(6,4),Vector2d(4,6)]:
            self.cells_dict[vec]=Cell(Wall(WallType(1),Directions(0)),[])

        self.cells_dict[Vector2d(1,2)] = Cell(Wall(WallType(2), Directions(1)), [])
        self.cells_dict[Vector2d(2,1)] = Cell(Wall(WallType(2), Directions(1)), [])

        self.cells_dict[Vector2d(3,6)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(4,5)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(5,4)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(6,3)] = Cell(Wall(WallType(2), Directions(5)), [])
        if location == "upper left":
            ...
        elif location == "upper right":
            new_dict={}
            for key in self.cells_dict.keys():
                new_dict[key]=self.cells_dict[Vector2d(9-key.y,key.x)]
                if new_dict[key].wall.type==WallType.HALF:
                    new_dict[key].wall.facing= Directions(((new_dict[key].wall.facing.to_int())-2)%8)
            self.cells_dict=new_dict
        elif location == "lower left":
            new_dict = {}
            for key in self.cells_dict.keys():
                new_dict[key] = self.cells_dict[Vector2d(key.y,9-key.x)]
                if new_dict[key].wall.type == WallType.HALF:
                    new_dict[key].wall.facing = Directions(((new_dict[key].wall.facing.to_int())+2)%8)
            self.cells_dict = new_dict
        elif location == "lower right":
            new_dict = {}
            for key in self.cells_dict.keys():
                new_dict[key] = self.cells_dict[Vector2d(9-key.x, 9-key.y)]
                if new_dict[key].wall.type == WallType.HALF:
                    new_dict[key].wall.facing= Directions(((new_dict[key].wall.facing.to_int())-4)%8)
            self.cells_dict = new_dict

    def generate_demo_straight(self,location:str, shop_tile=False):
        self.generate_demo_blank()
        if location == "up":
            for x in range(10):
                for y in [7, 8, 9]:
                    self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            for x,y in [(0,0),(0,1),(1,0),(0,2),(2,0),(1,1),(7,0),(8,0),(9,0),(8,1),(9,1),(9,2)]:
                self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            self.cells_dict[Vector2d(1, 2)] = Cell(Wall(WallType(2), Directions(1)), [])
            self.cells_dict[Vector2d(2, 1)] = Cell(Wall(WallType(2), Directions(1)), [])
            self.cells_dict[Vector2d(7, 1)] = Cell(Wall(WallType(2), Directions(7)), [])
            self.cells_dict[Vector2d(8, 2)] = Cell(Wall(WallType(2), Directions(7)), [])
        elif location=="down":
            for x in range(10):
                for y in [0, 1, 2]:
                    self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            for x,y in [(0,9),(0,8),(1,9),(0,7),(2,9),(1,8),(7,9),(8,9),(9,9),(8,8),(9,8),(9,7)]:
                self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            self.cells_dict[Vector2d(1, 7)] = Cell(Wall(WallType(2), Directions(3)), [])
            self.cells_dict[Vector2d(2, 8)] = Cell(Wall(WallType(2), Directions(3)), [])
            self.cells_dict[Vector2d(7, 8)] = Cell(Wall(WallType(2), Directions(5)), [])
            self.cells_dict[Vector2d(8, 7)] = Cell(Wall(WallType(2), Directions(5)), [])
        elif location=="left":
            for x in [0,1,2]:
                for y in range(10):
                    self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            for x,y in [(7,0),(7,9),(8,0),(8,1),(8,9),(8,8),(9,0),(9,1),(9,2),(9,9),(9,8),(9,7)]:
                self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            self.cells_dict[Vector2d(7, 8)] = Cell(Wall(WallType(2), Directions(5)), [])
            self.cells_dict[Vector2d(8, 7)] = Cell(Wall(WallType(2), Directions(5)), [])
            self.cells_dict[Vector2d(7, 1)] = Cell(Wall(WallType(2), Directions(7)), [])
            self.cells_dict[Vector2d(8, 2)] = Cell(Wall(WallType(2), Directions(7)), [])
        elif location=="right":
            for x in [7,8,9]:
                for y in range(10):
                    self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            for x,y in [(2,0),(2,9),(1,0),(1,1),(1,9),(1,8),(0,0),(0,1),(0,2),(0,9),(0,8),(0,7)]:
                self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
            self.cells_dict[Vector2d(1, 2)] = Cell(Wall(WallType(2), Directions(3)), [])
            self.cells_dict[Vector2d(2, 1)] = Cell(Wall(WallType(2), Directions(3)), [])
            self.cells_dict[Vector2d(1, 7)] = Cell(Wall(WallType(2), Directions(1)), [])
            self.cells_dict[Vector2d(2, 8)] = Cell(Wall(WallType(2), Directions(1)), [])

        if shop_tile:
            shop_item_cell=self.cells_dict[Vector2d(4+random.randint(0,1),4+random.randint(0,1))]
            if location == "up":
                shop_item_cell.shop_item=ShopItem(Armor("Rusty Armour","Usefull garbage",10,1),7)
            if location == "down":
                attacks=[Vector2d(x,y) for x,y in [(0,1),(0,2),(0,3),(1,0),(-1,0)]]
                shop_item_cell.shop_item = ShopItem(Weapon("Bloody Sword", "Designed for two-handed use",5,2,attacks),15)
            if location == "right":
                shop_item_cell.shop_item=ShopItem(HealingPotion("Healing Potion","For noobies",1,2),2)
            if location == "left":
                attacks = [Vector2d(x, y) for x, y in [(-2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1),(2,1),(2,0)]]
                shop_item_cell.shop_item=ShopItem(Weapon("Rusty Sword", "Strange invention of a novice blacksmith", 7, 2, attacks),10)
    def __hash__(self):
        return hash(self.lower_left_vector2d)

if __name__=="__main__":
    tile=Tile()
    tile.generate_demo_cross()
    print(tile[Vector2d(2,4)].wall.type)