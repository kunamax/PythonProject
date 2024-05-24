from ..Utility import Vector2d
from Utility import Directions
from ._tile import Tile
from ._cell import Cell
from ._wall import Wall, WallType
import random
from Entities import Entity
from Entities import Hero

class Map:
    def __init__(self, tiles_dictionary: dict[Vector2d, Tile]=None):
        self.tiles_dictionary = tiles_dictionary
        if self.tiles_dictionary==None:
            self.tiles_dictionary={}
        self.entities_list:list[Entity]=[]

    def __getitem__(self, item: Vector2d) -> Cell:
        return self.tiles_dictionary[Vector2d(item.x // 10, item.y // 10)].cells_dict[Vector2d(item.x % 10, item.y % 10)]
    
    def add_entity(self,entity:Entity)->None:
        self.entities_list.append(entity)
        self[entity.position].entities.append(entity)

    def perform_turn(self)->None:
        self._move()
        self._attack()
        
    def _move(self)->None:
        for ent in self.entities_list:
            self._move_entity(ent)
            #buy
            if self[ent.position].shop_item!=None and type(ent)==Hero and ent.money>=self[ent.position].shop_item.price:
                ent.add_item(self[ent.position].shop_item.item)
                ent.money-=self[ent.position].shop_item.price
                self[ent.position].shop_item=None


    def _attack(self)->None:
        for ent in self.entities_list:
            for position in ent.attack():
                for damaged_ent in self[position].entities:
                    damaged_ent.take_damage(ent.weapon.damage)
                    if not damaged_ent.alive:
                        ent.money+=damaged_ent.money
                        self.entities_list.pop(self.entities_list.index(damaged_ent))
                        self[position].entities.pop(self[position].entities.index(damaged_ent))
    def _move_entity(self,entity:Entity)->None:
        #next_cell_vector_candodate = entity.position + entity.current_direction.rotate_vector(entity.list_of_moves[entity.move_index].to_vector2d())
        if entity.current_direction == Directions.NORTH or entity.current_direction == Directions.SOUTH:
            next_cell_vector_candodate = entity.position + entity.current_direction.opposite.to_vector2d()
        else:
            next_cell_vector_candodate = entity.position + entity.current_direction.to_vector2d()
        next_wall = self[next_cell_vector_candodate].wall
        next_cell_vector = None

        if entity.on_wall:
            if next_wall.type == WallType.EMPTY:
                entity.on_wall = False
                next_cell_vector = next_cell_vector_candodate
            if next_wall.type == WallType.FULL:
                next_cell_vector = next_cell_vector_candodate
            if next_wall.type == WallType.HALF:
                next_cell_vector = entity.position
            if next_wall.type == WallType.STAIRS:
                entity.current_direction = next_wall.facing
                next_cell_vector = next_cell_vector_candodate
        else:
            if next_wall.type == WallType.EMPTY:
                next_cell_vector = next_cell_vector_candodate
            if next_wall.type == WallType.FULL:
                entity.current_direction = entity.current_direction.opposite
                next_cell_vector = entity.position

            if next_wall.type == WallType.HALF:
                if abs(entity.current_direction.to_int() - next_wall.facing.to_int())==1\
                        or abs(entity.current_direction.to_int() - next_wall.facing.to_int())==7:
                    entity.current_direction = entity.current_direction.opposite
                    next_cell_vector = entity.position
                else: #obroc
                    entity.current_direction=entity._handle_bouncle(entity.current_direction,next_wall.facing)
                    next_cell_vector = next_cell_vector_candodate

            if next_wall.type == WallType.STAIRS:
                if next_wall.facing == entity.current_direction:
                    entity.on_wall = True
                    next_cell_vector = next_cell_vector_candodate
                else:
                    entity.current_direction = entity.current_direction.opposite()
                    next_cell_vector = entity.position

        next_wall = self[next_cell_vector].wall
        if next_wall.type == WallType.HALF and entity.on_wall:
            if not (abs(entity.current_direction.to_int() - next_wall.facing.to_int())==1\
                        or abs(entity.current_direction.to_int() - next_wall.facing.to_int())==7):
                entity.current_direction = entity._handle_bouncle(entity.current_direction, next_wall.facing)
        self[entity.position].entities.pop( self[entity.position].entities.index(entity))
        entity.position=next_cell_vector
        self[entity.position].entities.append(entity)

    def generate_demo(self)->None:
        size = 2

        for x in range(-size, size + 1):
            for y in range(-size, size + 1):
                tile = Tile(Vector2d(x, y), {})
                for i in range(10):
                    for j in range(10):
                        if random.choices([True, False], [0.3, 0.7])[0] and not (i == 0 and j == 0):
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(1), Directions(0)), [])
                        elif i == 0 and j == 0:
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(0), Directions(0)), [])
                        else:
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(0), Directions(0)), [])
                self.tiles_dictionary[Vector2d(x, y)] = tile


        # self.tiles_dictionary[Vector2d(0, 0)].generate_demo_cross()
        #
        # self.tiles_dictionary[Vector2d(10, 0)].generate_demo_turn()
        # self.tiles_dictionary[Vector2d(0, 10)].generate_demo_turn()
        # self.tiles_dictionary[Vector2d(10, 10)].generate_demo_blank()
        #
        # self.tiles_dictionary[Vector2d(-10, 0)].generate_demo_cross()
        # self.tiles_dictionary[Vector2d(0, -10)].generate_demo_cross()
        # self.tiles_dictionary[Vector2d(-10, -10)].generate_demo_blank()
        #
        # self.tiles_dictionary[Vector2d(-10, 10)].generate_demo_cross()
        # self.tiles_dictionary[Vector2d(10, -10)].generate_demo_cross()


if __name__ == "__main__":
    size = 10
    ma = Map()
    ma.generate_demo()
    vec = Vector2d(11, -1)

    print(vec // 10)
    print(vec % 10)

    print(ma[vec].wall.type, ma[vec].wall.facing)
    print(ma.tiles_dictionary[vec // 10].lower_left_vector2d)
