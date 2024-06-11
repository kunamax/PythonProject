from Application.Map._map import Map
from Application.Map.Entities.Items.Utility import Vector2d
from .Map.map_maker import MapMaker

class GameEngine:
    def __init__(self):
        mm=MapMaker()
        self.size = 3
        self.map = mm.create_map(self.size)
        self.hero_position = Vector2d(2, 2)

    def go_to_shop(self,first_shop:bool=True):
        mm=MapMaker()
        if first_shop:
            self.hero_position = Vector2d(15, 15)
            self.map = mm.create_shop()
        else:
            self.hero_position = Vector2d(4, 4)
            self.map = mm.create_shop(first_shop=False)

    def go_to_boss(self):
        mm=MapMaker()
        self.hero_position = Vector2d(10, 9)
        self.map = mm.create_boss_arena()
