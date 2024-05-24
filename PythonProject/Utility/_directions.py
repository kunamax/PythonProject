from enum import Enum
from ._vector2d import Vector2d
class Directions(Enum):
    NORTH=0
    NORTH_EAST=1
    EAST=2
    SOUTH_EAST=3
    SOUTH=4
    SOUTH_WEST=5
    WEST=6
    NORTH_WEST=7

    @property
    def turn_right_90_degrees(self) :
        result = {
            Directions.NORTH: Directions.EAST,
            Directions.EAST: Directions.SOUTH,
            Directions.SOUTH: Directions.WEST,
            Directions.WEST: Directions.NORTH,
        }
        return result[self]

    @property
    def turn_left_90_degrees(self):
        result = {
            Directions.NORTH: Directions.WEST,
            Directions.WEST: Directions.SOUTH,
            Directions.SOUTH: Directions.EAST,
            Directions.EAST: Directions.NORTH
        }
        return result[self]

    @property
    def opposite(self):
        result = {
            Directions.NORTH: Directions.SOUTH,
            Directions.WEST: Directions.EAST,
            Directions.SOUTH: Directions.NORTH,
            Directions.EAST: Directions.WEST
        }
        return result[self]
    def to_vector2d(self)->Vector2d:
        result = {
            Directions.NORTH: Vector2d(0,1),
            Directions.EAST: Vector2d(1,0),
            Directions.SOUTH: Vector2d(0,-1),
            Directions.WEST: Vector2d(-1,0)
        }
        return result[self]
    def to_int(self)->int:
        result = {
        Directions.NORTH : 0,
        Directions.NORTH_EAST : 1,
        Directions.EAST : 2,
        Directions.SOUTH_EAST : 3,
        Directions.SOUTH : 4,
        Directions.SOUTH_WEST : 5,
        Directions.WEST : 6,
        Directions.NORTH_WEST : 7
        }
        return result[self]
    def rotate_vector(self, vector:Vector2d)->Vector2d:
        result = {
            Directions.NORTH: vector, # (0,1) -> (0,1)
            Directions.EAST: Vector2d(vector.y, -vector.x), # (1,0) -> (0,-1)
            Directions.SOUTH: Vector2d(-vector.x, -vector.y), # (0,-1) -> (0,-1)
            Directions.WEST: Vector2d(-vector.y, vector.x) # (-1,0) -> (0,1)
        }
        return result[self]