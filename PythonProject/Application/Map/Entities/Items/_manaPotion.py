from ._item import Item

class ManaPotion(Item):
    def __init__(self, name, description, weight, mana_amount):
        super().__init__(name, description, weight)
        self.mana_amount = mana_amount

    def use(self, hero):
        hero.inventory.remove(self)