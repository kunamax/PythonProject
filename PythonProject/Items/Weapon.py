from PythonProject.Items.Item import Item


class Weapon(Item):
    def __init__(self, name, description, weight, damage):
        super().__init__(name, description, weight)
        self.damage = damage
        self.equipped = False

    def use(self, hero):
        hero.equip_weapon(self)