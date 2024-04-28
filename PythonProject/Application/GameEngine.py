from Map.Floor import Floor
from Map.Wall import Wall
from Map.HeroOnMap import HeroOnMap

import random
import pygame

class GameEngine:
    def __init__(self):
        self.map = {}
        self.hero_position = (0, 3)
        for x in range(8):
            for y in range(6):
                if random.random() < 0.2 or x == 0 or x == 7 or y == 0 or y == 7:
                    self.map[(x, y)] = Wall(0, 1) # sample type and facing
                else:
                    self.map[(x, y)] = Floor()
                if (x, y) == self.hero_position:
                    self.map[(x, y)] = HeroOnMap(self.hero_position)

    def get_map(self):
        return self.map

    def set_map(self, new_map):
        self.map = new_map

    def get_hero_position(self):
        return self.hero_position

    def set_hero_position(self, new_position):
        self.hero_position = new_position

    def update_map(self, old_position, new_position):
        if old_position in self.map and isinstance(self.map[old_position], HeroOnMap) and new_position in self.map and not isinstance(self.map[new_position], Wall):
            self.map[old_position] = Floor()
            self.map[new_position] = HeroOnMap(new_position)
            self.hero_position = new_position
            return True
        else:
            return False

