from Entities.Entity import Entity

class Trap(Entity):
    def __init__(self,initiative,weapon,position,list_of_moves,max_health,direction):
        super().__init__(self,initiative,position,list_of_moves,max_health,direction)

    def deal_damage(self):
        super().deal_damage()
    def move(self):
        super().deal_damage()