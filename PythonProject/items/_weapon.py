from PythonProject.Items import Item


class Weapon(Item):
    def __init__(self, name, description, weight, damage, list_of_attacks: []):
        super().__init__(name, description, weight)
        self.damage = damage
        self.list_of_attacks = list_of_attacks
        self.equipped = False

    def equip(self, hero):
        hero.equip_weapon(self)