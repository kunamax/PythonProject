from ._entity import Entity
from Items import Armor
from Items import Weapon
from Utility import Vector2d
from Utility import Directions
import pygame


class Hero(Entity):
    def __init__(self, initiative: int, weapon: Weapon, armor: Armor, position: Vector2d,list_of_moves: list[Directions],
                 max_health: int, name: str = "Ziutek", direction: Directions = Directions.NORTH):
        super().__init__(initiative, position, list_of_moves, max_health, direction, weapon)
        self.name = name
        self.initiative = initiative
        self.armor = armor
        self.inventory = []
        self.alive = True

    def add_item(self, item)->None:
        self.inventory.append(item)

    def remove_item(self, item)->None:
        if item in self.inventory:
            self.inventory.remove(item)
            if isinstance(item, Weapon) and self.weapon == item:
                self.weapon = None
            if isinstance(item, Armor) and self.armor == item:
                self.armor = None

    def use_item(self, item)->None:
        if item in self.inventory:
            item.use(self)
            self.remove_item(item)

    def equip_weapon(self, weapon)->None:
        if weapon in self.inventory:
            if self.weapon:
                self.weapon.equipped = False
            self.weapon = weapon
            weapon.equipped = True

    def equip_armor(self, armor)->None:
        if armor in self.inventory:
            if self.armor:
                self.armor.equipped = False
            self.armor = armor
            armor.equipped = True

    # def take_damage(self,damage):
    #     self.current_health -= damage
    #     if self.current_health <= 0:
    #         self.alive = False

    def heal_damage(self, amount_of_healing)->None:
        self.current_health += amount_of_healing
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def draw(self, screen)->None:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.position[0], self.position[1], 50, 50))
