from Entities import Entity

class Enemy(Entity):
    def __init__(self, iniciative, position, list_of_moves, max_health, direction):
        self.super().__init__(self, iniciative, position, list_of_moves, max_health, direction)
    def deal_damage(self):
        self.super().deal_damage()
    def move(self):
        self.super().move()