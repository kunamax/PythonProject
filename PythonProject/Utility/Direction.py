from enum import Enum
from Utility.Vector2d import Vector2d
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


    def turn_left_90_degrees(self):
        result = {
            Directions.NORTH: Directions.WEST,
            Directions.WEST: Directions.SOUTH,
            Directions.SOUTH: Directions.EAST,
            Directions.EAST: Directions.NORTH
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