import random

from .Items.Utility import Directions
from .Items.Utility import Vector2d
from ._entity import Entity
from .Items import Weapon
from random import randint

class Enemy(Entity):
    def __init__(self, iniciative:int, position:Vector2d, list_of_moves:list[Directions],
                 max_health:int, direction:Directions,weapon:Weapon):
        super().__init__(iniciative, position, list_of_moves, max_health, direction,weapon)
        self.money = randint(2,5)
