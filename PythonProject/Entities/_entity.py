from abc import ABC as abc
from Utility import Vector2d
from Utility import Directions
from Application.Map._wall import WallType
from Items import Weapon
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
        self.weapon = weapon
        self.alive = True
        self.on_wall = False

    def move(self, map):
        # predict next vector
        self.move_index = (self.move_index + 1) % len(self.list_of_moves)
        next_cell_vector_candodate = self.position + self.current_direction.rotate_vector(self.list_of_moves[self.move_index].to_vector2d())
        next_wall = map[next_cell_vector_candodate].wall
        next_cell_vector = None

        if self.on_wall:
            if next_wall.type == WallType.EMPTY:
                self.on_wall = False
                next_cell_vector = next_cell_vector_candodate
            if next_wall.type == WallType.FULL:
                next_cell_vector = next_cell_vector_candodate
            if next_wall.type == WallType.HALF:
                next_cell_vector = self.position
            if next_wall.type == WallType.STAIRS:
                self.current_direction = next_wall.facing
                next_cell_vector = next_cell_vector_candodate
        else:
            if next_wall.type == WallType.EMPTY:
                next_cell_vector = next_cell_vector_candodate
            if next_wall.type == WallType.FULL:
                self.current_direction = self.current_direction.opposite
                next_cell_vector = self.position

            if next_wall.type == WallType.HALF:
                if abs(self.current_direction.to_int() - next_wall.facing.to_int())==1\
                        or abs(self.current_direction.to_int() - next_wall.facing.to_int())==7:
                    self.current_direction = self.current_direction.opposite
                    next_cell_vector = self.position
                else: #obroc
                    self.current_direction=self._handle_bouncle(self.current_direction,next_wall.facing)
                    next_cell_vector = next_cell_vector_candodate

            if next_wall.type == WallType.STAIRS:
                if next_wall.facing == self.current_direction:
                    self.on_wall = True
                    next_cell_vector = next_cell_vector_candodate
                else:
                    self.current_direction = self.current_direction.opposite()
                    next_cell_vector = self.position

        next_wall = map[next_cell_vector].wall
        if next_wall.type == WallType.HALF and self.on_wall:
            if not (abs(self.current_direction.to_int() - next_wall.facing.to_int())==1\
                        or abs(self.current_direction.to_int() - next_wall.facing.to_int())==7):
                self.current_direction = self._handle_bouncle(self.current_direction, next_wall.facing)

        map[self.position].entities.pop( map[self.position].entities.index(self))
        self.position=next_cell_vector
        map[self.position].entities.append(self)

    def _handle_bouncle(self,e_facing:Directions,w_facing:Directions)->Directions:
        tmp=e_facing.opposite.to_int()-w_facing.to_int()
        return Directions( (w_facing.to_int()-tmp)%8 )
    def attack(self, map) -> None:
        cells_to_attack = [self.position + self.current_direction.rotate_vector(attack) for attack in
                           self.weapon.list_of_attacks]
        for vec in cells_to_attack:
            for entity in map[vec].entities:
                entity.take_damage(self.weapon.damage)

    def take_damage(self, damage) -> None:
        self.current_health -= damage
        if self.current_health <= 0:
            self.alive = False
