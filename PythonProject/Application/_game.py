import random

import pygame

from Application.Map.Entities import Skeleton as Skel
from Application.Map.Entities import Hero, Enemy, Trap
from Application.Map.Entities.Items import Armor, Weapon, HealingPotion, ManaPotion
from Application import *
from Application.Map import WallType
from Application.Map.Entities.Items.Utility import Vector2d, Directions
from Application.Map import Deck

from time import sleep
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.window_rex_x = 1200
        self.window_rex_y = 800
        icon = pygame.image.load("Resources/hero.png")
        pygame.display.set_icon(icon)
        self.map_dimension_x = 800
        self.map_dimension_y = 800
        self.tile_size = 33
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.window_rex_x, self.window_rex_y))
        self.clock = pygame.time.Clock()
        self.scale = 100
        self.main_menu = MainMenu(self.screen)
        self.in_main_menu = True
        self.running = True
        self.paused = False
        self.hero = None
        self.enemies = []
        self.traps = []
        self.deck = Deck()
        self.selected_card_index = None
        self.selected_potion_index = None
        self.selected_equipment_index = None
        self.index_of_equipped_weapon = None
        self.index_of_equipped_armor = None
        self.placing_card = False
        self.images = {}
        self.move_counter = 0
        self.offset_x = 4
        self.offset_y = 4

        self.red_arrow_texture = pygame.image.load("Resources/red_arrow.png")
        self.pause_texture = pygame.image.load("Resources/pause_image.png")
        self.attack_texture = pygame.image.load("Resources/attack.png")
        self.spikes_texture = pygame.image.load("Resources/spikes.png")

        self.item_textures = {
            "Healing Potion": pygame.image.load("Resources/healing_potion.png"),
            "Mana Potion": pygame.image.load("Resources/mana_potion.png"),
            "Sword": pygame.image.load("Resources/sword.png"),
            "Armour": pygame.image.load("Resources/armour.png"),
            "Item": pygame.image.load("Resources/crate.png"),
            "Bloody Sword": pygame.image.load("Resources/sword1.png"),
            "Rusty Sword": pygame.image.load("Resources/sword2.png"),
            "Good Armour": pygame.image.load("Resources/armour1.png"),
            "Rusty Armour": pygame.image.load("Resources/armour2.png"),
            "Crate": pygame.image.load("Resources/crate.png")
        }

        self.entity_textures = {
            "Hero": pygame.image.load("Resources/hero.png"),
            "Regular Enemy": pygame.image.load("Resources/enemy.png"),
            "Trap": pygame.image.load("Resources/trap.png"),
            "Dedek": pygame.image.load("Resources/skeleton.png"),
            "Boss1": pygame.image.load("Resources/boss1.png"),
            "Boss2": pygame.image.load("Resources/boss2.png"),
        }

        self.wall_textures = {
            WallType.FULL: pygame.image.load("Resources/wall.jpg"),
            WallType.EMPTY: pygame.image.load("Resources/floor.jpg"),
            Directions.NORTH_EAST: pygame.image.load("Resources/half_wall1.png"),
            Directions.SOUTH_EAST: pygame.image.load("Resources/half_wall4.png"),
            Directions.SOUTH_WEST: pygame.image.load("Resources/half_wall2.png"),
            Directions.NORTH_WEST: pygame.image.load("Resources/half_wall3.png"),
            "Maze to Shop": pygame.image.load("Resources/teleport_maze_to_shop.png"),
            "Shop to Boss": pygame.image.load("Resources/teleport_shop_to_boss.png")
        }

        self.red_arrow_texture = pygame.transform.scale(self.red_arrow_texture, (self.scale, self.scale))
        self.attack_texture = pygame.transform.scale(self.attack_texture, (self.scale, self.scale))
        self.spikes_texture = pygame.transform.scale(self.spikes_texture, (self.scale, self.scale))

        self.pause_button = Button(800, 0, 200, 100, "Pause Game")
        self.quit_button = Button(800, 100, 200, 100, "Quit Game")
        self.reset_button = Button(800, 200, 200, 100, "Reset Game")
        self.resume_button = Button(500, 350, 200, 100, "Resume Game")
        self.potion_button = Button(1000, 0, 200, 100, "Use Potion")
        self.weapon_button = Button(1000, 100, 200, 100, "Equip Weapon")
        self.armor_button = Button(1000, 200, 200, 100, "Equip Armor")
        self.new_game_button = Button(500, 400, 200, 100, "New Game")
        self.game_over = False

        self.game_engine = GameEngine()
        self.hero_position = Vector2d(2, 2)

    def run(self):
        self.game_engine = GameEngine()
        self.hero_position = Vector2d(2, 2)
        self.deck.generate_cards(5)
        weapon = Weapon("Sword", "A sharp blade", 10, 5, [Vector2d(0, 1),
                                                          Vector2d(1, 1), Vector2d(-1, 1), Vector2d(0, 2),
                                                          Vector2d(1, 2), Vector2d(-1, 2)])
        armor = Armor("Armour", "A sturdy armour", 15, 3)
        position = Vector2d(self.game_engine.hero_position.x, self.game_engine.hero_position.y)
        list_of_moves = []
        max_health = 100
        direction = Directions.SOUTH
        self.create_character("Hero", 1, weapon, armor, position, list_of_moves, max_health, direction)
        self.game_engine.map.add_entity(self.hero)
        healing_potion1 = HealingPotion("Healing Potion", "A potion that heals you", 10, 5)
        healing_potion2 = HealingPotion("Healing Potion", "A potion that heals you", 10, 5)
        mana_potion1 = ManaPotion("Mana Potion", "A potion that restores mana", 10, 5)
        mana_potion2 = ManaPotion("Mana Potion", "A potion that restores mana", 10, 5)
        self.hero.add_item(healing_potion1)
        self.hero.add_item(mana_potion1)
        self.hero.add_item(healing_potion2)
        self.hero.add_item(mana_potion2)
        self.hero.inventory.append(weapon)
        self.hero.inventory.append(armor)

        self.hero_money = self.hero.money

        self.place_enemies(15, 5)

        self.checkpoint_shop = Vector2d(5, 5)
        self.in_maze = True
        self.in_boss = False
        self.in_shop = False

        weapon1 = Weapon("Bloody Sword", "A bloody sword", 10, 10, [Vector2d(0, 1)])
        armor1 = Armor("Good Armour", "A sturdy armour", 15, 3)
        weapon2 = Weapon("Rusty Sword", "A bloody sword", 10, 10, [Vector2d(0, 1)])
        armor2 = Armor("Rusty Armour", "A sturdy armour", 15, 3)

        self.hero.inventory.append(weapon1)
        self.hero.inventory.append(armor1)
        self.hero.inventory.append(weapon2)
        self.hero.inventory.append(armor2)


        self.equip_weapon(weapon)
        self.equip_armor(armor)

        self.set_offset()
        self.inventory_size = len(self.hero.inventory)

        while self.running:
            if self.in_main_menu:
                self.main_menu.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.main_menu.handle_events(event):
                            self.in_main_menu = False
                            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, self.window_rex_x, self.window_rex_y))
            else:
                self.set_offset()
                self.handle_events()
                self.draw()
                self.update()
            self.clock.tick(60)
            sleep(0.01)
        pygame.quit()

    # def initialize_game(self):


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

                items = self.hero.inventory
                items_per_row = 2
                item_width, item_height = 100, 50
                start_x, start_y = 1000, 300

                for i, item in enumerate(items):
                    row = i // items_per_row
                    col = i % items_per_row
                    x = start_x + col * item_width
                    y = start_y + row * item_height
                    item_rect = pygame.Rect(x, y, item_width, item_height)
                    if item_rect.collidepoint(mouse_pos):
                        print(f"Item {i} clicked")
                        self.selected_equipment_index = i
                        return
                if (self.selected_card_index is not None and self.placing_card and mouse_pos[0] < self.map_dimension_x
                        and mouse_pos[1] < self.map_dimension_y and mouse_pos[0] > 0 and mouse_pos[1] > 0):
                    map_pos = Vector2d(mouse_pos[0] // self.tile_size - self.offset_x,
                                       mouse_pos[1] // self.tile_size - self.offset_y)
                    if (self.game_engine.map[map_pos].wall.type == WallType.EMPTY
                            and self.game_engine.map[map_pos].entities == []):
                        selected_card = self.deck.cards[self.selected_card_index]
                        print(selected_card.wall.type, selected_card.wall.facing)
                        self.game_engine.map[map_pos].wall.type = selected_card.wall.type
                        self.game_engine.map[map_pos].wall.facing = selected_card.wall.facing
                        self.deck.cards.pop(self.selected_card_index)
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
                    self.screen.fill((0, 0, 0))
                    self.run()
                elif self.resume_button.is_clicked(event):
                    self.paused = False
                elif self.potion_button.is_clicked(event):
                    if self.selected_equipment_index is not None:
                        selected_item = self.hero.inventory[self.selected_equipment_index]
                        if isinstance(selected_item, HealingPotion) or isinstance(selected_item, ManaPotion):
                            self.use_potion(selected_item)
                            if isinstance(selected_item, ManaPotion):
                                self.deck.add_cards_any(1)
                            self.selected_equipment_index = None
                            print("Potion used")
                elif self.weapon_button.is_clicked(event):
                    if self.selected_equipment_index is not None:
                        selected_item = self.hero.inventory[self.selected_equipment_index]
                        if isinstance(selected_item, Weapon):
                            self.equip_weapon(selected_item)
                            print("Weapon equipped")
                            self.index_of_equipped_weapon = self.selected_equipment_index
                            self.selected_equipment_index = None
                elif self.armor_button.is_clicked(event):
                    if self.selected_equipment_index is not None:
                        selected_item = self.hero.inventory[self.selected_equipment_index]
                        if isinstance(selected_item, Armor):
                            self.equip_armor(selected_item)
                            print("Armor equipped")
                            self.index_of_equipped_armor = self.selected_equipment_index
                            self.selected_equipment_index = None
                elif self.new_game_button.is_clicked(event):
                    if self.game_over:
                        self.game_over = False
                        pygame.display.flip()
                        self.screen.fill((0, 0, 0))
                        self.run()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.move_counter = 0
                    self.hero.list_of_moves = [Directions.SOUTH] * 5
                    for enemy in self.enemies:
                        enemy.list_of_moves = [Directions.NORTH] * 5
                if self.game_engine.map[self.hero.position].wall.type != WallType.HALF:
                    if event.key == pygame.K_UP:
                        self.hero.current_direction = Directions.NORTH
                    elif event.key == pygame.K_DOWN:
                        self.hero.current_direction = Directions.SOUTH
                    elif event.key == pygame.K_LEFT:
                        self.hero.current_direction = Directions.WEST
                    elif event.key == pygame.K_RIGHT:
                        self.hero.current_direction = Directions.EAST

    def set_offset(self):
        hero_global_x, hero_global_y = self.hero.position.x, self.hero.position.y
        screen_center_x = self.window_rex_x / self.scale
        screen_center_y = self.window_rex_y / self.scale
        self.offset_x = screen_center_x - hero_global_x
        self.offset_y = screen_center_y - hero_global_y + 3

    def update(self):
        if self.hero.current_health <= 0:
            self.game_over = True
            return

        if self.hero.list_of_moves:
            self.draw_attack()
            self.hero_attacking = True
            self.game_engine.map.perform_turn()
            self.move_counter += 1
            if self.move_counter == 5:
                self.hero.list_of_moves = []
        for enemy in self.enemies:
            if enemy.list_of_moves:
                enemy.list_of_moves.pop(0)
        self.set_offset()

        if len(self.hero.inventory) > self.inventory_size and self.hero.money != self.hero_money:
            self.display_message("You bought an item!")
            self.inventory_size = len(self.hero.inventory)
            self.hero_money = self.hero.money
        elif len(self.hero.inventory) == self.inventory_size and self.hero.money == self.hero_money and self.game_engine.map[self.hero.position].shop_item:
            print(self.hero_position)
            self.display_message("Not enough money!")

        if self.hero.position == self.checkpoint_shop:
            if self.in_maze:
                self.go_to_shop()
            elif self.in_shop:
                self.go_to_boss()
            elif self.in_boss:
                self.go_to_maze()

    def go_to_shop(self):
        self.transition_screen()
        self.in_maze = False
        self.in_boss = False
        self.in_shop = True
        pygame.display.flip()
        self.game_engine.go_to_shop()
        self.hero.position = Vector2d(15, 15)
        self.game_engine.map.add_entity(self.hero)
        self.checkpoint_shop = Vector2d(15, 29)

    def go_to_boss(self):
        self.transition_screen()
        self.in_maze = False
        self.in_shop = False
        self.in_boss = True
        pygame.display.flip()
        self.game_engine.go_to_boss()
        self.hero.position = Vector2d(10, 9)
        self.game_engine.map.add_entity(self.hero)
        self.checkpoint_shop = Vector2d(5, 5)
        min_x, max_x, min_y, max_y = self.game_engine.map.map_dimensions()

        name = random.choice(["Boss1", "Boss2"])

        while True:
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            position = Vector2d(x, y)

            if self.game_engine.map[position].wall.type != WallType.EMPTY:
                continue

            enemy_list_of_moves = [Directions.NORTH]
            enemy_max_health = 20
            enemy_direction = Directions.SOUTH
            weapon = Weapon("Claws", "Sharp claws", 10, 5,
                            [Vector2d(0, 1), Vector2d(1, 1), Vector2d(-1, 1), Vector2d(0, 2)])
            boss = Enemy(name, 1, position, enemy_list_of_moves, enemy_max_health, enemy_direction, weapon)

            self.game_engine.map.add_entity(boss)
            print(f"Boss placed at {position}")
            break

    def go_to_maze(self):
        self.transition_screen()
        self.in_boss = False
        self.in_shop = False
        self.in_maze = True
        self.run()

    def transition_screen(self):
        transition_image = pygame.image.load("Resources/pause_image.png")
        transition_image = pygame.transform.scale(transition_image, (self.window_rex_x, self.window_rex_y))

        black_rect = pygame.Surface((self.window_rex_x, self.window_rex_y))
        black_rect.fill((0, 0, 0))
        self.screen.blit(black_rect, (0, 0))
        pygame.display.flip()

        self.screen.blit(transition_image, (0, 0))
        pygame.display.flip()

        pygame.time.wait(1000)

        self.screen.blit(black_rect, (0, 0))
        pygame.display.flip()
        pass

    def draw_pause_screen(self):
        overlay = pygame.Surface((self.window_rex_x, self.window_rex_y))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(60)
        self.screen.blit(overlay, (0, 0))
        self.resume_button.draw(self.screen)
        pygame.display.flip()

    def draw(self):
        if self.paused:
            self.draw_pause_screen()
        elif self.game_over:
            self.draw_game_over_screen()
        else:
            self.draw_map()
            self.draw_cards()
            self.draw_items()
            self.draw_character_info()
            self.pause_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.reset_button.draw(self.screen)
            self.potion_button.draw(self.screen)
            self.weapon_button.draw(self.screen)
            self.armor_button.draw(self.screen)
            self.clear_areas_outside_map()
        pygame.display.flip()

    def draw_map(self):
        map = self.game_engine.map
        scale = 3

        pygame.display.flip()

        boss_x = boss_y = 0
        boss = None

        for tile_position, tile in map.tiles_dictionary.items():
            for cell_position, cell in tile.cells_dict.items():
                cells_in_tile = self.game_engine.map.cells_in_tile
                global_x, global_y = tile_position.x * cells_in_tile + cell_position.x, tile_position.y * cells_in_tile + cell_position.y
                x, y = (global_x + self.offset_x) / scale, (global_y + self.offset_y) / scale
                if cell.wall.type == WallType.FULL or cell.wall.type == WallType.EMPTY:
                    self.screen.blit(
                        pygame.transform.scale(self.wall_textures[cell.wall.type], (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                elif cell.wall.type == WallType.HALF:
                    self.screen.blit(
                        pygame.transform.scale(self.wall_textures[WallType.EMPTY], (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                    self.screen.blit(
                        pygame.transform.scale(self.wall_textures[cell.wall.facing], (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                for entity in cell.entities:
                    if hasattr(entity, 'attack'):
                        if isinstance(entity, Hero):
                            self.screen.blit(
                                pygame.transform.scale(
                                    pygame.transform.rotate(self.red_arrow_texture, entity.current_direction.angle()),
                                    (self.scale // scale, self.scale // scale)),
                                (x * self.scale, y * self.scale))
                        if entity.name == "Boss1" or entity.name == "Boss2":
                            boss = entity.name
                            boss_x, boss_y = x, y
                        else:
                            self.screen.blit(
                                pygame.transform.scale(self.entity_textures[entity.name], (self.scale // scale, self.scale // scale)),
                                (x * self.scale, y * self.scale))
                if global_x == self.checkpoint_shop.x and global_y == self.checkpoint_shop.y:
                    if self.in_maze:
                        self.screen.blit(
                            pygame.transform.scale(self.wall_textures["Maze to Shop"], (self.scale // scale, self.scale // scale)),
                            (x * self.scale, y * self.scale))
                    elif self.in_shop:
                        self.screen.blit(
                            pygame.transform.scale(self.wall_textures["Shop to Boss"], (self.scale // scale, self.scale // scale)),
                            (x * self.scale, y * self.scale))
                if cell.shop_item:
                    self.screen.blit(
                        pygame.transform.scale(self.item_textures[cell.shop_item.item.name], (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                    price = cell.shop_item.price
                    price_text = self.font.render(str(price), True, (0, 0, 0))
                    self.screen.blit(price_text, (x * self.scale, y * self.scale))
        size = (self.scale // scale) * 4
        if boss:
            self.screen.blit(
                pygame.transform.scale(self.entity_textures[boss], (size, size)),
                (boss_x * self.scale, boss_y * self.scale))

    def draw_character_info(self):
        font = pygame.font.Font(None, 36)

        hp_text = font.render(f"HP: {self.hero.current_health}", True, (255, 255, 255))
        gold_text = font.render(f"Gold: {self.hero.money}", True, (255, 255, 255))
        position_text = font.render(f"Position: {self.hero.position}", True, (255, 255, 255))

        weapon_text = font.render(f"Weapon: {self.hero.weapon.name if self.hero.weapon else 'None'}", True,
                                  (255, 255, 255))
        armor_text = font.render(f"Armor: {self.hero.armor.name if self.hero.armor else 'None'}", True, (255, 255, 255))

        text_x = self.window_rex_x - 200
        hp_text_y = self.window_rex_y - 150
        gold_text_y = self.window_rex_y - 120
        position_text_y = self.window_rex_y - 90
        weapon_text_y = self.window_rex_y - 60
        armor_text_y = self.window_rex_y - 30

        self.screen.blit(hp_text, (text_x, hp_text_y))
        self.screen.blit(gold_text, (text_x, gold_text_y))
        self.screen.blit(position_text, (text_x, position_text_y))
        self.screen.blit(weapon_text, (text_x, weapon_text_y))
        self.screen.blit(armor_text, (text_x, armor_text_y))

    def place_enemies(self, num_enemies = 15, num_traps = 5):
        min_x, max_x, min_y, max_y = self.game_engine.map.map_dimensions()
        for _ in range(num_enemies):
            while True:
                x = randint(min_x, max_x)
                y = randint(min_y, max_y)
                position = Vector2d(x, y)

                if self.game_engine.map[position].wall.type != WallType.EMPTY:
                    continue

                enemy_list_of_moves = [Directions.NORTH]
                enemy_max_health = 20
                enemy_direction = Directions.SOUTH
                weapon = Weapon("Claws", "Sharp claws", 10, 5,
                                [Vector2d(0, 1), Vector2d(1, 1), Vector2d(-1, 1), Vector2d(0, 2)])
                enemy = Enemy("Regular Enemy", 1, position, enemy_list_of_moves, enemy_max_health, enemy_direction, weapon)
                self.game_engine.map.add_entity(enemy)
                print(f"Enemy placed at {position}")
                break
        for _ in range(num_traps):
            while True:
                x = randint(min_x, max_x)
                y = randint(min_y, max_y)
                position = Vector2d(x, y)

                if self.game_engine.map[position].wall.type != WallType.EMPTY:
                    continue

                weapon = Weapon("Claws", "Sharp claws", 10, 5, [Vector2d(0, 1), Vector2d(1, 1), Vector2d(-1, 1), Vector2d(0, 2)])

                trap = Trap("Trap", 1, Vector2d(x, y), [], 10, Directions.NORTH, weapon)
                self.game_engine.map.add_entity(trap)
                self.traps.append(trap)
                break

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
        self.hero.use_item(potion)

    def display_message(self, message): # 1, 14 bug
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.map_dimension_x / 2, self.map_dimension_y / 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.draw.rect(self.screen, (0, 0, 0), text_rect)

    def draw_game_over_screen(self):
        overlay = pygame.Surface((self.window_rex_x, self.window_rex_y))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(60)
        self.screen.blit(overlay, (0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.window_rex_x / 2, self.map_dimension_y / 4))
        self.screen.blit(game_over_text, text_rect)
        self.new_game_button.draw(self.screen)
        pygame.display.flip()

    def draw_cards(self):
        cards_per_row = 2
        card_width, card_height = 100, 50
        start_x, start_y = 800, 300

        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(800, 0, 400, 800))

        for i, card in enumerate(self.deck.cards):
            if card.wall.type == WallType.HALF:
                row = i // cards_per_row
                col = i % cards_per_row
                x = start_x + col * card_width
                y = start_y + row * card_height
                if i == self.selected_card_index:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x, y, card_width, card_height), 3)
                self.screen.blit(pygame.transform.scale(self.wall_textures[card.wall.facing], (card_width, card_height)), (x, y))

    def draw_items(self):
        items_per_row = 2
        item_width, item_height = 100, 50
        start_x, start_y = 1000, 300

        items = self.hero.inventory

        for i, item in enumerate(items):
            row = i // items_per_row
            col = i % items_per_row
            x = start_x + col * item_width
            y = start_y + row * item_height
            self.screen.blit(pygame.transform.scale(self.item_textures[item.name], (item_width, item_height)), (x, y))
            if i == self.selected_equipment_index:
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, item_width, item_height), 3)
            if i == self.index_of_equipped_weapon:
                pygame.draw.rect(self.screen, (255, 00, 255), (x, y, item_width, item_height), 3)
            if i == self.index_of_equipped_armor:
                pygame.draw.rect(self.screen, (0, 0, 255), (x, y, item_width, item_height), 3)

    def draw_attack(self):
        scale = 3

        if self.in_shop:
            return

        for entity in self.game_engine.map.entities_list:
            if hasattr(entity, 'attack'):
                list_of_attacks = entity.attack()

                for i in list_of_attacks:
                    if self.game_engine.map[i].wall.type != WallType.EMPTY:
                        continue
                    x2, y2 = (i.x + self.offset_x) / scale, (i.y + self.offset_y) / scale

                    if x2 * self.scale < 0 or y2 * self.scale < 0 or x2 * self.scale > self.map_dimension_x - 30:
                        continue

                    if isinstance(entity, Hero):
                        self.screen.blit(pygame.transform.scale(self.attack_texture, (self.tile_size, self.tile_size)),
                                         (x2 * self.scale, y2 * self.scale))
                    elif isinstance(entity, Trap) or isinstance(entity, Enemy):
                        self.screen.blit(pygame.transform.scale(self.spikes_texture, (self.tile_size, self.tile_size)),
                                         (x2 * self.scale, y2 * self.scale))

    def clear_areas_outside_map(self):
        map_left_pixel, map_right_pixel, map_top_pixel, map_bottom_pixel = self.map_screen_dimensions()
        if map_left_pixel > 0:
            self.screen.fill((0, 0, 0), (0, 0, map_left_pixel, self.map_dimension_y))
        if map_right_pixel < self.window_rex_x:
            self.screen.fill((0, 0, 0), (map_right_pixel, 0, self.map_dimension_x - map_right_pixel, self.map_dimension_y))
        if map_top_pixel > 0:
            self.screen.fill((0, 0, 0), (0, 0, self.map_dimension_x, map_top_pixel))
        if map_bottom_pixel < self.window_rex_y:
            self.screen.fill((0, 0, 0), (0, map_bottom_pixel, self.map_dimension_x, self.window_rex_y - map_bottom_pixel))

    def map_screen_dimensions(self):
        scale = 3
        min_x, max_x, min_y, max_y = self.game_engine.map.map_dimensions()
        return (min_x + self.offset_x) * (self.scale // scale), (max_x + self.offset_x) * (self.scale // scale), (min_y + self.offset_y) * (self.scale // scale), (max_y + self.offset_y) * (self.scale // scale)


if __name__ == "__main__":
    game = Game()
    game.run()