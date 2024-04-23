import pygame

from entities import Hero
from items import HealingPotion
from items import Armor
from items import Weapon
from application import Button
from application import Text


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.hero = None

        self.create_button = Button(50, 50, 200, 50, "Create Character")
        self.equip_weapon_button = Button(50, 110, 200, 50, "Equip Weapon")
        self.equip_armor_button = Button(50, 170, 200, 50, "Equip Armor")
        self.character_text = Text(50, 230, "")

    def run(self):
        weapon = Weapon("Sword", "A sharp blade", 10, 5)
        armor = Armor("Shield", "A sturdy shield", 15, 3)
        position = (0, 0)
        list_of_moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        max_health = 100
        direction = "right"
        self.create_character("Hero", 1, weapon, armor, position, list_of_moves, max_health, direction)

        self.equip_weapon(weapon)
        self.equip_armor(armor)

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.create_button.is_clicked(event):
                    weapon = Weapon("Sword", "A sharp blade", 10, 5)
                    armor = Armor("Shield", "A sturdy shield", 15, 3)
                    position = (0, 0)
                    list_of_moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    max_health = 100
                    direction = "right"
                    self.create_character("Hero", 1, weapon, armor, position, list_of_moves, max_health, direction)
                    self.character_text.text = weapon.name + " and " + armor.name + " equipped"
                elif self.equip_weapon_button.is_clicked(event):
                    weapon = Weapon("Axe", "A heavy axe", 15, 7)
                    self.equip_weapon(weapon)
                    self.character_text.text = "Weapon equipped"
                elif self.equip_armor_button.is_clicked(event):
                    armor = Armor("Plate", "A sturdy plate armor", 20, 5)
                    self.equip_armor(armor)
                    self.character_text.text = "Armor equipped"

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.create_button.draw(self.screen)
        self.equip_weapon_button.draw(self.screen)
        self.equip_armor_button.draw(self.screen)
        self.character_text.draw(self.screen)
        if self.hero:
            self.hero.draw(self.screen)
        pygame.display.flip()

    def add_item(self, item):
        if self.hero:
            self.hero.add_item(item)

    def create_character(self, name, initiative, weapon, armor, position, list_of_moves, max_health, direction):
        self.hero = Hero(initiative, weapon, armor, position, list_of_moves, max_health, name, direction)
        self.hero.add_item(weapon)
        self.hero.add_item(armor)

    def create_item(self, item_class, *args):
        item = item_class(*args)
        self.hero.add_item(item)

    def equip_weapon(self, weapon):
        if self.hero and isinstance(weapon, Weapon):
            self.hero.equip_weapon(weapon)

    def equip_armor(self, armor):
        if self.hero and isinstance(armor, Armor):
            self.hero.equip_armor(armor)

    def use_potion(self, potion):
        if self.hero and isinstance(potion, HealingPotion):
            self.hero.use_item(potion)


if __name__ == "__main__":
    game = Game()
    game.run()