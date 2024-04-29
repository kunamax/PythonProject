from PythonProject.Entities.Entity import Entity

class Trap(Entity):
    def __init__(self,initiative,position,list_of_moves,max_health,direction,weapon):
        super().__init__(self,initiative,position,list_of_moves,max_health,direction,weapon)

    def take_damage(self,damage) ->None:
        #traps are unkillable
        pass