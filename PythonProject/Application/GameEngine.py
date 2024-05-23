from Application.Map._map import Map
from Application.Map._wall import WallType
from Application.Map.Entities import Hero
from Utility import Vector2d


class GameEngine:
    def __init__(self):
        self.map = Map()
        self.hero_position = Vector2d(0, 0)
        self.map.generate_demo()
        print(self.map[Vector2d(9, 9)].wall.type)

    def get_map(self):
        return self.map

    def set_map(self, new_map):
        self.map = new_map

    def get_hero_position(self):
        return self.hero_position

    def set_hero_position(self, new_position):
        self.hero_position = new_position

    def update_map(self, old_position, new_position):
        old_cell = self.map[old_position]
        new_cell = self.map[new_position]
        if old_cell is not None and new_cell is not None and new_cell.wall.type == WallType.EMPTY:
            old_cell.entities = [entity for entity in old_cell.entities if not isinstance(entity, Hero)]
            new_cell.entities.append(self.map[old_position])
            self.hero_position = new_position
            return True
        return False