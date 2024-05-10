from ._item import Item


class Armor(Item):
    def __init__(self, name, description, weight, defense):
        super().__init__(name, description, weight)
        self.defense = defense
        self.equipped = False

    def use(self, hero):
        hero.equip_armor(self)