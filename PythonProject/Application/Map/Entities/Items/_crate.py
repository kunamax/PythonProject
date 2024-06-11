from ._item import Item


class Crate(Item):
    def __init__(self, name, description, weight):
        super().__init__(name, description, weight)

    def use(self, hero):
        hero.inventory.remove(self)
        print("Crate collected!")