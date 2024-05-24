from Application.Map._map import Map
from Utility import Vector2d


class GameEngine:
    def __init__(self):
        self.map = Map()
        self.hero_position = Vector2d(0, 0)
        self.map.generate_demo()