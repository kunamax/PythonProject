from Application.Map._map import Map
from Application.Map.Entities.Items.Utility import Vector2d
from .Map.map_maker import MapMaker

class GameEngine:
    def __init__(self):
        mm=MapMaker()
        self.map = mm.create_map(4)
        self.hero_position = Vector2d(2, 2)
        # self.map.generate_demo()
        # self.map.generate_demo_shop()

    def go_to_shop(self):
        mm=MapMaker()
        self.hero_position = Vector2d(15, 15)
        # self.map = mm.create_shop(False)
        self.map = mm.create_boss_arena()

    def go_to_boss(self):
        mm=MapMaker()
        self.hero_position = Vector2d(4, 4)
        self.map = mm.create_boss_arena()
