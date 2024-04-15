from abc import ABC as abc
from Utility.Vector2d import Vector2d
from typing import List
from Utility.Directions import Directions
from Map.Wall import Wall, WallType

class Entity(abc):
    def __init__(self,initiative,position,list_of_moves,max_health,direction,weapon):
        self.initiative=initiative
        self.position=position
        self.list_of_moves=list_of_moves#directions list
        self.move_index=-1
        self.current_health = max_health
        self.max_health = max_health
        self.current_direction = direction
        self.weapon=weapon
        self.alive = True
        self.on_wall=False

    def move(self,map)->Vector2d:
        #predict next vector
        self.move_index = (self.move_index + 1) % len(self.list_of_moves)
        next_cell_vector_candodate=self.position+self.list_of_moves[self.move_index].to_vector2d()
        next_wall=map[Vector2d(next_cell_vector_candodate.x//10,next_cell_vector_candodate.y//10)]\
        [Vector2d(next_cell_vector_candodate.x,next_cell_vector_candodate.y)]
        next_cell_vector=None
        
        
        if self.on_wall:
            if next_wall.type == WallType.EMPTY:
                self.on_wall=False
                next_cell_vector= next_cell_vector_candodate
            if next_wall.type == WallType.FULL:
                next_cell_vector= next_cell_vector_candodate
            if next_wall.type == WallType.HALF:
                next_cell_vector=self.position
            if next_wall.type == WallType.STAIRS:
                self.current_direction=next_wall.facing[1]
                next_cell_vector= next_cell_vector_candodate
        else:
            if next_wall.type == WallType.EMPTY:
                next_cell_vector= next_cell_vector_candodate
            if next_wall.type == WallType.FULL:
                self.current_direction=self.current_direction.opposite()
                next_cell_vector= self.position
            if next_wall.type == WallType.HALF:
                if self.current_direction in next_wall.facing:
                    self.current_direction = self.current_direction.opposite()
                    next_cell_vector= self.position
                else:
                    if next_wall.facing[0].opposite()==self.current_direction:
                        self.current_direction=next_wall.facing[1]
                    else:
                        self.current_direction=next_wall.facing[0]
                next_cell_vector= next_cell_vector_candodate
            if next_wall.type == WallType.STAIRS:
                if next_wall.facing[0].opposite()==self.current_direction:
                    self.on_wall=True
                    next_cell_vector= next_cell_vector_candodate
                else:
                    self.current_direction = self.current_direction.opposite()
                    next_cell_vector= self.position
        next_wall=map[Vector2d(next_cell_vector.x//10,next_cell_vector.y//10)]\
        [Vector2d(next_cell_vector.x,next_cell_vector.y)]
        if next_wall.type==WallType.HALF:
            if self.current_direction in next_wall.facing:
                return next_cell_vector
            else:
                if next_wall.facing[0].opposite() == self.current_direction:
                    self.current_direction = next_wall.facing[1]
                else:
                    self.current_direction = next_wall.facing[0]
            return next_cell_vector

    def attack(self)->  List[Vector2d]:
        return [self.position+attack.rotate_to(self.current_direction) for attack in self.weapon.list_of_attacks]


    def deal_damage(self):
        pass

    def take_damage(self,damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.alive = False
