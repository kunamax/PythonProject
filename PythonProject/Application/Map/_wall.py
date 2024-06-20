from enum import IntEnum
from .Entities.Items.Utility import Directions
class WallType(IntEnum):
    EMPTY=0
    FULL=1
    HALF=2
class Wall:
    '''
    type=0: facing doesn't matter
    type=1: facing doesn't matter
    type=2: facing is direction in which the tile is empty
    '''
    def __init__(self,type:WallType,facing:Directions):
        self.type=type
        self.facing=facing
