from enum import Enum

class WallType(Enum):
    EMPTY=0
    FULL=1
    HALF=2
    STAIRS=3

class Wall:
    '''
    type=0: facing doesn't matter but should be None
    type=1: facing doesn't matter but should be None
    type=2: facing is a pair of directions witch hero will bounce
    type=3: facing is a par of directions witch:
                                                first is start of stairs
                                                second is end of stairs
    '''
    def __init__(self,type,facing):
        self.type=type
        self.facing=facing
        #TODO: here will be a assertion error check about length of facing list
