from ._item import Item
from .Utility import Vector2d


class Weapon(Item):
    def __init__(self, name, description, weight, damage,list_of_attacks:list[Vector2d]):
        super().__init__(name, description, weight)
        self.damage = damage
        self.equipped = False

    def use(self, hero):
        hero.equip_weapon(self)