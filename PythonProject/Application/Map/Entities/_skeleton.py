class Skeleton():
    def __init__(self, name, position, direction):
        self.name = name
        self.position = position
        self.direction = direction
        self.list_of_moves = []
        self.list_of_attacks = []
        self.money = 0
        self.interaction = False

    def attack(self):
        return []