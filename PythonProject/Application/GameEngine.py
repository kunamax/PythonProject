from Application.Map._map import Map
from Application.Map._wall import WallType
from Application.Map._heroOnMap import HeroOnMap
from Utility import Vector2d


class GameEngine:
    def __init__(self):
        self.map = Map()
        self.hero_position = Vector2d(0, 0)
        self.map.generate_demo()
        print(self.map[Vector2d(9, 9)].wall.type)

        starting_tile = self.map.tiles_dictionary[self.hero_position // 10]
        starting_cell = starting_tile.cells_dict[self.hero_position % 10]
        starting_cell.entities.append(HeroOnMap(self.hero_position))

    def get_map(self):
        return self.map

    def set_map(self, new_map):
        self.map = new_map

    def get_hero_position(self):
        return self.hero_position

    def set_hero_position(self, new_position):
        self.hero_position = new_position

    def update_map(self, old_position, new_position):
        old_tile = self.map.tiles_dictionary.get(old_position // 10)
        new_tile = self.map.tiles_dictionary.get(new_position // 10)
        if old_tile is not None and new_tile is not None:
            old_cell = old_tile.cells_dict.get(old_position % 10)
            new_cell = new_tile.cells_dict.get(new_position % 10)
            if old_cell is not None and new_cell is not None and not new_cell.wall.type == WallType.FULL:
                old_cell.entities = [entity for entity in old_cell.entities if not isinstance(entity, HeroOnMap)]
                new_cell.entities.append(HeroOnMap(new_position))
                self.hero_position = new_position
                return True
        return False