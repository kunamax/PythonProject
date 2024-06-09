from ._entity import Entity

class Trap(Entity):
    def __init__(self,name,initiative,position,list_of_moves,max_health,direction,weapon):
        super().__init__(initiative,position,list_of_moves,max_health,direction,weapon)
        self.name=name

    def take_damage(self,damage) ->None:
        #traps are unkillable
        pass