from Entities import Entity

class Enemy(Entity):
    def __init__(self, iniciative, position, list_of_moves, max_health, direction,weapon):
        self.super().__init__(self, iniciative, position, list_of_moves, max_health, direction,weapon)
    def deal_damage(self):
        self.super().deal_damage()