from Entities import Entity
class Hero (Entity):
    def __init__(self,iniciative,weapon,position,list_of_moves,max_health,
                armor,name="Ziutek",
                 direction = "tutaj bedzie enum",initiative=0):
        self.super().__init__(iniciative,weapon,position,list_of_moves,max_health,direction)
        self.name = name
        self.armor = armor
        self.iniciative=initiative

    def change_weapon(self,weapon):
        self.weapon = weapon

    def change_armor(self,armor):
        self.armor = armor

    def take_damage(self,damage):
        self.current_health -= damage

    def heal_damage(self,amount_of_healing):
        self.current_health += amount_of_healing



