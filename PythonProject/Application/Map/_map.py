from ._tile import Tile
from ._cell import Cell
from ._wall import Wall, WallType
import random
from .Entities import Entity, Hero, Skeleton, Enemy, Trap
from .Entities.Items.Utility import Vector2d, Directions

class Map:
    def __init__(self, tiles_dictionary: dict[Vector2d, Tile]=None):
        self.tiles_dictionary = tiles_dictionary
        self.cells_in_tile = 10
        if self.tiles_dictionary==None:
            self.tiles_dictionary={}
        self.entities_list:list[Entity]=[]

    def __getitem__(self, item: Vector2d) -> Cell:
        try:
            return self.tiles_dictionary[Vector2d(item.x // self.cells_in_tile, item.y
                                              // self.cells_in_tile)].cells_dict[Vector2d(item.x % self.cells_in_tile, item.y % self.cells_in_tile)]
        except KeyError:
            print("KeyError", item)
            return Cell(Wall(WallType.FULL, Directions.NORTH), [])
    def add_entity(self,entity:Entity)->None:
        self.entities_list.append(entity)
        self[entity.position].entities.append(entity)

    def map_dimensions(self) -> tuple[int, int, int, int]:
        min_x = min(tile_position.x for tile_position in self.tiles_dictionary.keys()) * self.cells_in_tile
        max_x = (max(tile_position.x for tile_position in self.tiles_dictionary.keys()) * self.cells_in_tile) + self.cells_in_tile
        min_y = min(tile_position.y for tile_position in self.tiles_dictionary.keys()) * self.cells_in_tile
        max_y = (max(tile_position.y for tile_position in self.tiles_dictionary.keys()) * self.cells_in_tile) + self.cells_in_tile
        return min_x, max_x, min_y, max_y
    def perform_turn(self)->None:
        self.__move()
        self.__attack()

    def __move(self)->None:
        for ent in self.entities_list:
            self.__move_entity(ent)
            #buy
            if self[ent.position].shop_item!=None and type(ent)==Hero and ent.money>=self[ent.position].shop_item.price:
                ent.add_item(self[ent.position].shop_item.item)
                ent.money-=self[ent.position].shop_item.price
                self[ent.position].shop_item=None

    def __attack(self)->None:
        for ent in self.entities_list:
            if not ent.interaction:
                break
            for position in ent.attack():

                for damaged_ent in self[position].entities:
                    if (not damaged_ent.interaction or (isinstance(damaged_ent,Enemy) and isinstance(ent,Enemy)) or
                            (isinstance(damaged_ent, Enemy) and isinstance(ent,Trap)) or
                            (isinstance(damaged_ent, Trap) and isinstance(ent,Enemy))):
                        break
                    damaged_ent.take_damage(ent.weapon.damage)
                    if not damaged_ent.alive:
                        print("Died")
                        ent.money+=damaged_ent.money
                        self.entities_list.pop(self.entities_list.index(damaged_ent))
                        self[position].entities.pop(self[position].entities.index(damaged_ent))
                        skeleton = Skeleton("Dedek", position, Directions.NORTH)
                        self.entities_list.append(skeleton)
                        self[position].entities.append(skeleton)
    def __move_entity(self,entity:Entity)->None:
        if not entity.list_of_moves:
            return
        if isinstance(entity, Enemy):
            entity.random_direction()
            entity.random_direction()
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
                entity.on_wall = True
            if next_wall.type == WallType.HALF:
                next_cell_vector = entity.position
                entity.on_wall = True
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

        if next_wall.type == WallType.FULL and entity.on_wall:
            entity.current_direction = entity._handle_bouncle(entity.current_direction.opposite.to_int() + self[entity.position].wall.facing.to_int() + 1, next_wall.facing)

        min_x, max_x, min_y, max_y = self.map_dimensions()
        if min_x <= next_cell_vector.x <= max_x and min_y <= next_cell_vector.y <= max_y:
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
                        if (x == size and i == 9) or (x == -size and i == 0) or (y == size and j == 9) or (y == -size and j == 0):
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType.FULL, Directions(0)), [])
                        elif random.choices([True, False], [0.1, 0.9])[0] and not (i == 0 and j == 0):
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(1), Directions(0)), [])
                        elif i == 0 and j == 0:
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(0), Directions(0)), [])
                        else:
                            tile.cells_dict[Vector2d(i, j)] = Cell(Wall(WallType(0), Directions(0)), [])
                self.tiles_dictionary[Vector2d(x, y)] = tile
    def generate_demo_shop(self) -> None:
        self.tiles_dictionary[Vector2d(-1, -1)]=Tile(Vector2d(-1,-1),{})
        self.tiles_dictionary[Vector2d(-1, 0)]=Tile(Vector2d(-1,0),{})
        self.tiles_dictionary[Vector2d(-1, 1)]=Tile(Vector2d(-1,1),{})
        self.tiles_dictionary[Vector2d(0, 1)]=Tile(Vector2d(0,1),{})
        self.tiles_dictionary[Vector2d(0, 0)]=Tile(Vector2d(0,0),{})
        self.tiles_dictionary[Vector2d(0, -1)]=Tile(Vector2d(0,-1),{})
        self.tiles_dictionary[Vector2d(1, -1)]=Tile(Vector2d(1,-1),{})
        self.tiles_dictionary[Vector2d(1, 0)]=Tile(Vector2d(1,0),{})
        self.tiles_dictionary[Vector2d(1, 1)]=Tile(Vector2d(1,1),{})

        self.tiles_dictionary[Vector2d(-1, -1)].generate_demo_turn("lower right")
        self.tiles_dictionary[Vector2d(-1, 0)].generate_demo_straight("left", shop_tile=True)
        self.tiles_dictionary[Vector2d(-1, 1)].generate_demo_turn("upper right")
        self.tiles_dictionary[Vector2d(0, 1)].generate_demo_straight("down", shop_tile=True)
        self.tiles_dictionary[Vector2d(0, 0)].generate_demo_cross()
        self.tiles_dictionary[Vector2d(0, -1)].generate_demo_straight("up", shop_tile=True)
        self.tiles_dictionary[Vector2d(1, -1)].generate_demo_turn("lower left")
        self.tiles_dictionary[Vector2d(1, 0)].generate_demo_straight("right", shop_tile=True)
        self.tiles_dictionary[Vector2d(1, 1)].generate_demo_turn("upper left")



if __name__ == "__main__":
    size = 10
    ma = Map()
    ma.generate_demo()
    vec = Vector2d(11, -1)

    print(vec // 10)
    print(vec % 10)

    print(ma[vec].wall.type, ma[vec].wall.facing)
    print(ma.tiles_dictionary[vec // 10].lower_left_vector2d)
