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
        self.interaction = True


    def get_next_move(self):
        self.move_index= (self.move_index+1) % len(self.list_of_moves)
        return self.current_direction.rotate_vector(self.list_of_moves[self.move_index].to_vector2d())
    def attack(self) -> list[Vector2d]:
        cells_to_attack = [self.position + self.current_direction.rotate_vector(attack) for attack in
                           self.weapon.list_of_attacks]
        return cells_to_attack
    def take_damage(self, damage) -> None:
        self.current_health -= damage
        if self.current_health <= 0:
            self.alive = False