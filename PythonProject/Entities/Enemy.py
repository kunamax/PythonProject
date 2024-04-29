from PythonProject.Utility.Directions import Directions
from PythonProject.Utility.Vector2d import Vector2d
from PythonProject.Entities.Entity import Entity
from PythonProject.Items.Weapon import Weapon

class Enemy(Entity):
    def __init__(self, iniciative:int, position:Vector2d, list_of_moves:list[Directions],
                 max_health:int, direction:Directions,weapon:Weapon):
        super().__init__(self, iniciative, position, list_of_moves, max_health, direction,weapon)