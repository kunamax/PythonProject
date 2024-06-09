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
        self.map = Map()
        self.hero_position = Vector2d(5, -10)
        self.map.generate_demo_shop()