from abc import ABC as abc
from .Items.Utility import Vector2d
from .Items.Utility import Directions
from .Items import Weapon
from random import randint
class Entity(abc):
    def __init__(self, initiative: int, position: Vector2d, list_of_moves: list[Directions],
                 max_health: int, direction: Directions, weapon: Weapon):
        self.initiative = initiative
        self.position = position
        self.list_of_moves = list_of_moves
        self.move_index = -1
        self.current_health = max_health
        self.max_health = max_health
        self.current_direction = direction
        self.money:int=randint(2,5)
        self.weapon = weapon
        self.alive = True
        self.on_wall = False

    def _handle_bouncle(self,e_facing:Directions,w_facing:Directions)->Directions:
        tmp=e_facing.opposite.to_int()-w_facing.to_int()
        return Directions( (w_facing.to_int()-tmp)%8 )
    def attack(self) -> list[Vector2d]:
        cells_to_attack = [self.position + self.current_direction.rotate_vector(attack) for attack in
                           self.weapon.list_of_attacks]
        return cells_to_attack
    def take_damage(self, damage) -> None:
        self.current_health -= damage
        if self.current_health <= 0:
            self.alive = False
