class Character:
    def __init__(self, name="Ziutek", current_health = 10, max_health = 10, weapon="Rust sword", armor="No armor", direction = "tutaj bedzie enum"):
        self.name = name
        self.current_health = current_health
        self.max_health = max_health
        self.weapon = weapon
        self.armor = armor
        self.direction = direction

    def change_weapon(self,weapon):
        self.weapon = weapon

    def change_armor(self,armor):
        self.armor = armor

    def take_damage(self,damage):
        self.current_health -= damage

    def heal_damage(self,amount_of_healing):
        self.current_health += amount_of_healing

    def change_direction(self,wall_type):
        pass

