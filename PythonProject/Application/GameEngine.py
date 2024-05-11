from Map._map import Map
from Map._tile import Tile
from Map._cell import Cell
from Map._wall import Wall, WallType
from Map._heroOnMap import HeroOnMap
from Utility import Vector2d

import random
import pygame

class GameEngine:
    def __init__(self):
        self.map = Map()
        self.hero_position = Vector2d(0, 0)
        self.map.generate_demo()

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
        if new_position // 10 in self.map.tiles_dictionary and not self.map[new_position].wall.type == WallType.FULL:

            old_tile = self.map.tiles_dictionary[old_position // 10]
            old_cell = old_tile.cells_dict[old_position % 10]
            old_cell.entities = [entity for entity in old_cell.entities if not isinstance(entity, HeroOnMap)]

            new_tile = self.map.tiles_dictionary[new_position // 10]
            new_cell = new_tile.cells_dict[new_position % 10]
            new_cell.entities.append(HeroOnMap(new_position))

            self.hero_position = new_position
            return True
        else:
            return False