from random import choice
from Utility import Directions
from ._card import Card


class Deck:
    def __init__(self):
        self.cards = []

    def generate_cards(self, num_cards):
        allowed_directions = [Directions.NORTH_EAST, Directions.NORTH_WEST, Directions.SOUTH_EAST,
                              Directions.SOUTH_WEST]
        for _ in range(num_cards):
            from Application.Map import Wall, WallType
            wall_direction = choice(allowed_directions)
            wall = Wall(WallType.HALF, wall_direction)
            card = Card(wall)
            self.cards.append(card)