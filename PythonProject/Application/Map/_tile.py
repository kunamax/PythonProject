import random
from .Entities.Items import Armor,Weapon,HealingPotion,ShopItem
from .Entities.Items.Utility import Vector2d, Directions
from ._cell import Cell
from ._wall import Wall,WallType
class Tile:
    def __init__(self,lower_left_vector2d:Vector2d,cells_dict:dict[Vector2d,Cell]):
        self.cells_dict=cells_dict
        self.lower_left_vector2d=lower_left_vector2d
    def __getitem__(self, item:Vector2d)->Cell:
        return self.cells_dict[item]
    def __hash__(self):
        return hash(self.lower_left_vector2d)