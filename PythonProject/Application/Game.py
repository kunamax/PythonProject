import pygame
from Entities.Hero import Hero
from Items.HealingPotion import HealingPotion
from Items.Armor import Armor
from Items.Weapon import Weapon
from Application.Button import Button
from Application.Text import Text
from Application.GameEngine import GameEngine
from Map.Wall import Wall
from Map.Floor import Floor
from Map.HeroOnMap import HeroOnMap


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.scale = 100
        self.running = True
        self.hero = None

        self.create_button = Button(50, 50, 200, 50, "Create Character")
        self.equip_weapon_button = Button(50, 110, 200, 50, "Equip Weapon")
        self.equip_armor_button = Button(50, 170, 200, 50, "Equip Armor")
        self.character_text = Text(50, 230, "")
        self.game_engine = GameEngine()

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
        # self.screen.fill((0, 0, 0))
        self.draw_map()
        # self.create_button.draw(self.screen)
        # self.equip_weapon_button.draw(self.screen)
        # self.equip_armor_button.draw(self.screen)
        # self.character_text.draw(self.screen)
        # if self.hero:
        #     self.hero.draw(self.screen)
        pygame.display.flip()

    def draw_map(self):
        map = self.game_engine.get_map()
        for position, tile in map.items():
            x, y = position
            if isinstance(tile, Wall):
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))
            elif isinstance(tile, Floor):
                pygame.draw.rect(self.screen, (0, 50, 0), pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))
            elif isinstance(tile, HeroOnMap):
                pygame.draw.circle(self.screen, (255, 0, 0), (x * self.scale + self.scale // 2, y * self.scale + self.scale // 2), self.scale // 2)

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