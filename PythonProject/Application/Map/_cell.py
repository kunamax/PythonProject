from .Entities import Entity
from ._wall import Wall
from Items import ShopItem
class Cell:
    def __init__(self,wall:Wall,entities:list[Entity],shop_item:ShopItem=None):
    # shop_item=Null:ShopItem do sprawdzenia
        self.wall=wall
        self.entities=entities
        self.shop_item=shop_item