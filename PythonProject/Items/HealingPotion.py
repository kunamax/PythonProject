from PythonProject.Items.Item import Item

class HealingPotion(Item):
    def __init__(self, name, description, weight, heal_amount):
        super().__init__(name, description, weight)
        self.heal_amount = heal_amount

    def use(self, hero):
        hero.heal(self.heal_amount)