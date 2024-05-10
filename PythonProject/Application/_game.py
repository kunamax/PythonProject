import pygame
from Entities import Hero
from Items import HealingPotion
from Items import Armor
from Items import Weapon
from _button import Button
from Text import Text
from GameEngine import GameEngine
from Map import Wall
from Map import Floor
from Map import HeroOnMap
import time


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.scale = 100
        self.running = True
        self.paused = False
        self.hero = None

        self.wall_texture = pygame.image.load("Resources/wall.jpg")
        self.floor_texture = pygame.image.load("Resources/floor.jpg")
        self.hero_texture = pygame.image.load("Resources/hero.png")
        self.wall_texture = pygame.transform.scale(self.wall_texture, (self.scale, self.scale))
        self.floor_texture = pygame.transform.scale(self.floor_texture, (self.scale, self.scale))
        self.hero_texture = pygame.transform.scale(self.hero_texture, (self.scale, self.scale))

        self.pause_button = Button(800, 0, 200, 100, "Pause Game")
        self.quit_button = Button(800, 100, 200, 100, "Quit Game")
        self.reset_button = Button(800, 200, 200, 100, "Reset Game")
        self.resume_button = Button(400, 300, 200, 100, "Resume Game")

        self.game_engine = GameEngine()

    def run(self):
        weapon = Weapon("Sword", "A sharp blade", 10, 5, [(0, 1), (1, 1), (-1, 1), (0, 2)])
        armor = Armor("Shield", "A sturdy shield", 15, 3)
        position = (0, 3)
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
                if self.pause_button.is_clicked(event):
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                        self.draw_pause_screen()
                elif self.quit_button.is_clicked(event):
                    pygame.quit()
                    quit()
                elif self.reset_button.is_clicked(event):
                    self.game_engine = GameEngine()
                    self.set_position((0, 3))
                elif self.resume_button.is_clicked(event):
                    self.paused = False
            elif event.type == pygame.KEYDOWN and not self.paused:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    while True:
                        new_position = (self.hero.position[0], self.hero.position[1] - 1)
                        if not self.game_engine.update_map(self.hero.position, new_position):
                            break
                        self.hero.position = new_position
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    while True:
                        new_position = (self.hero.position[0], self.hero.position[1] + 1)
                        if not self.game_engine.update_map(self.hero.position, new_position):
                            break
                        self.hero.position = new_position
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    while True:
                        new_position = (self.hero.position[0] - 1, self.hero.position[1])
                        if not self.game_engine.update_map(self.hero.position, new_position):
                            break
                        self.hero.position = new_position
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    while True:
                        new_position = (self.hero.position[0] + 1, self.hero.position[1])
                        if not self.game_engine.update_map(self.hero.position, new_position):
                            break
                        self.hero.position = new_position
                print(self.hero.position)


    def update(self):
        pass

    def draw_pause_screen(self):
        overlay = pygame.Surface((1000, 800))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(60)
        self.screen.blit(overlay, (0, 0))
        self.resume_button.draw(self.screen)
        #self.pause_text.draw(self.screen)
        pygame.display.flip()

    def draw(self):
        if self.paused:
            self.draw_pause_screen()
        else:
            self.draw_map()
            self.pause_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.reset_button.draw(self.screen)
        pygame.display.flip()

    def draw_map(self):
        map = self.game_engine.get_map()
        for position, tile in map.items():
            x, y = position
            if isinstance(tile, Wall):
                self.screen.blit(self.wall_texture, (x*self.scale, y*self.scale))
            elif isinstance(tile, Floor):
                self.screen.blit(self.floor_texture, (x*self.scale, y*self.scale))
            elif isinstance(tile, HeroOnMap):
                self.screen.blit(self.hero_texture, (x*self.scale, y*self.scale))

    def add_item(self, item):
        if self.hero:
            self.hero.add_item(item)

    def create_character(self, name, initiative, weapon, armor, position, list_of_moves, max_health, direction):
        self.hero = Hero(initiative, weapon, armor, position, list_of_moves, max_health, name, direction)
        self.hero.add_item(weapon)
        self.hero.add_item(armor)

    def set_position(self, position):
        self.hero.position = position

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