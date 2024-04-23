from entities import Entity

class Trap(Entity):
    def __init__(self,initiative,position,list_of_moves,max_health,direction,weapon):
        super().__init__(self,initiative,position,list_of_moves,max_health,direction,weapon)