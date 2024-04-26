from _entity import Entity

class Enemy(Entity):
    def __init__(self, iniciative, position, list_of_moves, max_health, direction,weapon):
        super().__init__(self, iniciative, position, list_of_moves, max_health, direction,weapon)