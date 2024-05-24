from Utility import Directions
from Utility import Vector2d
from ._entity import Entity
from Items import Weapon

class Enemy(Entity):
    def __init__(self, iniciative:int, position:Vector2d, list_of_moves:list[Directions],
                 max_health:int, direction:Directions,weapon:Weapon):
        super().__init__(iniciative, position, list_of_moves, max_health, direction, weapon)

