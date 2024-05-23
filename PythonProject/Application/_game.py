import pygame
from Map.Entities import Hero
from Map.Entities.Items import HealingPotion
from Map.Entities.Items import Armor
from Map.Entities.Items import Weapon
from _button import Button
from GameEngine import GameEngine
from Application.Map import WallType
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
        self.selected_card_index = None
        self.placing_card = False
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
                mouse_pos = pygame.mouse.get_pos()
                for i, card in enumerate(self.deck.cards):
                    row = i // 2
                    col = i % 2
                    x = 800 + col * 100
                    y = 300 + row * 50
                    card_rect = pygame.Rect(x, y, 100, 50)
                    if card_rect.collidepoint(mouse_pos):
                        print(f"Card {i} clicked")
                        self.selected_card_index = i
                        self.placing_card = True
                        return
                if self.selected_card_index is not None and self.placing_card:
                    tile_size = 33
                    map_pos = Vector2d(mouse_pos[0] // tile_size, mouse_pos[1] // tile_size)
                    if self.game_engine.get_map()[map_pos].wall.type == WallType.EMPTY:
                        selected_card = self.deck.cards[self.selected_card_index]
                        self.game_engine.get_map()[map_pos].wall.type = selected_card.wall.type
                        self.game_engine.get_map()[map_pos].wall.facing = selected_card.wall.facing
                        self.selected_card_index = None
                        self.placing_card = False
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
                elif cell.wall.type == WallType.HALF:
                    image = self.images[cell.wall.type][cell.wall.facing]
                    self.screen.blit(
                        pygame.transform.scale(image, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                elif cell.wall.type == WallType.EMPTY:
                    self.screen.blit(
                        pygame.transform.scale(self.floor_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                if any(isinstance(entity, Hero) for entity in cell.entities):
                    self.screen.blit(
                        pygame.transform.scale(self.hero_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
        if not any(isinstance(entity, Hero) for entity in map[self.hero_position].entities):
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
        cards_per_row = 2
        card_width, card_height = 100, 50
        start_x, start_y = 800, 300

        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(800, 300, 200, len(self.deck.cards) * 100))

        for i, card in enumerate(self.deck.cards):
            if card.wall.type == WallType.HALF:
                row = i // cards_per_row
                col = i % cards_per_row
                x = start_x + col * card_width
                y = start_y + row * card_height
                image = self.images[card.wall.type][card.wall.facing]
                scaled_image = pygame.transform.scale(image, (card_width, card_height))
                if i == self.selected_card_index:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, card_width, card_height), 3)
                self.screen.blit(scaled_image, (x, y))



if __name__ == "__main__":
    game = Game()
    game.run()