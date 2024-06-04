from enum import Enum
from .Entities.Items.Utility import Directions
class WallType(Enum):
    EMPTY=0
    FULL=1
    HALF=2
    STAIRS=3

class Wall:
    '''
    type=0: facing doesn't matter
    type=1: facing doesn't matter
    type=2: facing is direction in with the tile is empty
    type=3: facing is direction in with hero will be getting higher
    '''
    def __init__(self,type:WallType,facing:Directions):
        self.type=type
        self.facing=facing
        #TODO: here will be a assertion error check about length of facing list
