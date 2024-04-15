from abc import ABC as abc
from Utility.Vector2d import Vector2d
from typing import List

class Entity(abc):
    def __init__(self,initiative,position,list_of_moves,max_health,direction):
        self.initiative=initiative
        self.position=position
        self.list_of_moves=list_of_moves#directions list
        self.move_index=-1
        self.current_health = max_health
        self.max_health = max_health
        self.current_direction = direction
        self.alive = True
    def move(self)->Vector2d:
        self.move_index=(self.move_index+1)%len(self.list_of_moves)
        return self.position+self.list_of_moves[self.move_index].to_vector2d()
    def attack(self)->  List[Vector2d]:
        return [self.position+attack.rotate_to(self.current_direction) for attack in self.weapon.list_of_attacks]
    def change_direction(self,wall_type):
        #some swith
        pass

    def deal_damage(self):
        pass

    def take_damage(self,damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.alive = False
