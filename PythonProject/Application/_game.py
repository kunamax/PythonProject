import pygame
from Map.Entities import Hero
from Map.Entities.Items import HealingPotion
from Map.Entities.Items import Armor
from Map.Entities.Items import Weapon
from _button import Button
from GameEngine import GameEngine
from Application.Map import WallType
from Application.Map import HeroOnMap
from Utility import Vector2d, Directions
from Items import Deck


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.scale = 100
        self.running = True
        self.paused = False
        self.hero = None
        self.deck = Deck()
        self.deck.generate_cards(5)
        self.images = {}

        self.wall_texture = pygame.image.load("Resources/wall.jpg")
        self.floor_texture = pygame.image.load("Resources/floor.jpg")
        self.hero_texture = pygame.image.load("Resources/hero.png")
        self.half_wall1_texture = pygame.image.load("Resources/half_wall1.png")
        self.half_wall2_texture = pygame.image.load("Resources/half_wall2.png")
        self.wall_texture = pygame.transform.scale(self.wall_texture, (self.scale, self.scale))
        self.floor_texture = pygame.transform.scale(self.floor_texture, (self.scale, self.scale))
        self.hero_texture = pygame.transform.scale(self.hero_texture, (self.scale, self.scale))
        self.half_wall1_texture = pygame.transform.scale(self.half_wall1_texture, (self.scale, self.scale))
        self.half_wall2_texture = pygame.transform.scale(self.half_wall2_texture, (self.scale, self.scale))

        self.images = {
            WallType.HALF: {
                Directions.NORTH_EAST: pygame.transform.scale(pygame.image.load("Resources/half_wall1.png"),
                                                         (self.scale, self.scale)),
                Directions.SOUTH_EAST: pygame.transform.scale(pygame.image.load("Resources/half_wall4.png"),
                                                         (self.scale, self.scale)),
                Directions.SOUTH_WEST: pygame.transform.scale(pygame.image.load("Resources/half_wall2.png"),
                                                            (self.scale, self.scale)),
                Directions.NORTH_WEST: pygame.transform.scale(pygame.image.load("Resources/half_wall3.png"),
                                                            (self.scale, self.scale)),
            },
        }

        self.pause_button = Button(800, 0, 200, 100, "Pause Game")
        self.quit_button = Button(800, 100, 200, 100, "Quit Game")
        self.reset_button = Button(800, 200, 200, 100, "Reset Game")
        self.resume_button = Button(400, 300, 200, 100, "Resume Game")

        self.game_engine = GameEngine()
        self.hero_position = Vector2d(0, 0)
        self.game_engine.set_hero_position(self.hero_position)

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
                    self.hero_position = Vector2d(0, 0)
                    self.game_engine.set_hero_position(self.hero_position)
                elif self.resume_button.is_clicked(event):
                    self.paused = False
            elif event.type == pygame.KEYDOWN and not self.paused:
                new_position = self.hero_position
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    new_position = Vector2d(self.hero_position.x, self.hero_position.y - 1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    new_position = Vector2d(self.hero_position.x, self.hero_position.y + 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    new_position = Vector2d(self.hero_position.x - 1, self.hero_position.y)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    new_position = Vector2d(self.hero_position.x + 1, self.hero_position.y)
                print(self.hero_position)
                print(new_position)
                new_cell = self.game_engine.get_map()[new_position]
                print(self.game_engine.get_map()[new_position].wall.type)
                if new_cell is not None and not new_cell.wall.type == WallType.FULL:
                    print(self.game_engine.update_map(self.hero_position, new_position))
                    if self.game_engine.update_map(self.hero_position, new_position):
                        self.hero_position = new_position

    def update(self):
        pass

    def draw_pause_screen(self):
        overlay = pygame.Surface((1000, 800))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(60)
        self.screen.blit(overlay, (0, 0))
        self.resume_button.draw(self.screen)
        pygame.display.flip()

    def draw(self):
        if self.paused:
            self.draw_pause_screen()
        else:
            self.draw_map()
            self.draw_cards()
            self.pause_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.reset_button.draw(self.screen)
        pygame.display.flip()

    def draw_map(self):
        map = self.game_engine.get_map()
        scale = 3
        for tile_position, tile in map.tiles_dictionary.items():
            for cell_position, cell in tile.cells_dict.items():
                global_x, global_y = tile_position.x * 10 + cell_position.x, tile_position.y * 10 + cell_position.y
                x, y = global_x / scale, global_y / scale
                if cell.wall.type == WallType.FULL:
                    self.screen.blit(
                        pygame.transform.scale(self.wall_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                elif cell.wall.type == WallType.EMPTY:
                    self.screen.blit(
                        pygame.transform.scale(self.floor_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                if any(isinstance(entity, HeroOnMap) for entity in cell.entities):
                    self.screen.blit(
                        pygame.transform.scale(self.hero_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
        if not any(isinstance(entity, HeroOnMap) for entity in map[self.hero_position].entities):
            x, y = (self.hero_position.x) / scale, (self.hero_position.y) / scale
            self.screen.blit(
                pygame.transform.scale(self.hero_texture, (self.scale // scale, self.scale // scale)),
                (x * self.scale, y * self.scale))

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

    def draw_cards(self):
        for i, card in enumerate(self.deck.cards):
            if card.wall.type == WallType.HALF:
                image = self.images[card.wall.type][card.wall.facing]
                self.screen.blit(image, (700, 50 + i * 100))

    def get_tiles_between(self, old_position, new_position):
        tiles = []
        x0, y0 = old_position.x, old_position.y
        x1, y1 = new_position.x, new_position.y
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                tiles.append(Vector2d(x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                tiles.append(Vector2d(x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        tiles.append(Vector2d(x, y))
        return tiles



if __name__ == "__main__":
    game = Game()
    game.run()