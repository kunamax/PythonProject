import pygame

from Application.Map.Entities import Skeleton as Skel
from Application.Map.Entities import *
from Application.Map.Entities.Items import *
from Map.Entities.Items import HealingPotion
from Map.Entities.Items import Armor
from Map.Entities.Items import Weapon
from _button import Button
from _gameEngine import GameEngine
from Application.Map import WallType
from Application.Map.Entities.Items.Utility import Vector2d, Directions
from Items import Deck

from time import sleep
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.window_rex_x = 1200
        self.window_rex_y = 800
        self.map_dimension_x = 800
        self.map_dimension_y = 800
        self.tile_size = 33
        self.screen = pygame.display.set_mode((self.window_rex_x, self.window_rex_y))
        self.clock = pygame.time.Clock()
        self.scale = 100
        self.running = True
        self.paused = False
        self.hero = None
        self.enemies = []
        self.traps = []
        self.deck = Deck()
        self.deck.generate_cards(5)
        self.selected_card_index = None
        self.selected_potion_index = None
        self.selected_equipment_index = None
        self.placing_card = False
        self.images = {}
        self.move_counter = 0
        self.offset_x = 4
        self.offset_y = 4

        self.wall_texture = pygame.image.load("Resources/wall.jpg")
        self.floor_texture = pygame.image.load("Resources/floor.jpg")
        self.hero_texture = pygame.image.load("Resources/hero.png")
        self.enemy_texture = pygame.image.load("Resources/enemy.png")
        self.trap_texture = pygame.image.load("Resources/trap.png")
        self.skeleton_texture = pygame.image.load("Resources/skeleton.png")
        self.red_arrow_texture = pygame.image.load("Resources/red_arrow.png")
        self.half_wall1_texture = pygame.image.load("Resources/half_wall1.png")
        self.half_wall2_texture = pygame.image.load("Resources/half_wall2.png")
        self.healing_potion_texture = pygame.image.load("Resources/healing_potion.png")
        self.mana_potion_texture = pygame.image.load("Resources/mana_potion.png")
        self.sword_texture = pygame.image.load("Resources/sword.png")
        self.armour_texture = pygame.image.load("Resources/armour.png")
        self.pause_texture = pygame.image.load("Resources/pause_image.png")
        self.waves_texture = pygame.image.load("Resources/waves.png")
        self.wall_texture = pygame.transform.scale(self.wall_texture, (self.scale, self.scale))
        self.floor_texture = pygame.transform.scale(self.floor_texture, (self.scale, self.scale))
        self.hero_texture = pygame.transform.scale(self.hero_texture, (self.scale, self.scale))
        self.half_wall1_texture = pygame.transform.scale(self.half_wall1_texture, (self.scale, self.scale))
        self.half_wall2_texture = pygame.transform.scale(self.half_wall2_texture, (self.scale, self.scale))
        self.enemy_texture = pygame.transform.scale(self.enemy_texture, (self.scale, self.scale))
        self.trap_texture = pygame.transform.scale(self.trap_texture, (self.scale, self.scale))
        self.skeleton_texture = pygame.transform.scale(self.skeleton_texture, (self.scale, self.scale))
        self.red_arrow_texture = pygame.transform.scale(self.red_arrow_texture, (self.scale, self.scale))
        self.healing_potion_texture = pygame.transform.scale(self.healing_potion_texture, (self.scale, self.scale))
        self.mana_potion_texture = pygame.transform.scale(self.mana_potion_texture, (self.scale, self.scale))
        self.sword_texture = pygame.transform.scale(self.sword_texture, (self.scale, self.scale))
        self.armour_texture = pygame.transform.scale(self.armour_texture, (self.scale, self.scale))
        # self.waves_texture = pygame.transform.scale(self.waves_texture, (self.scale, self.scale))

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
        self.resume_button = Button(500, 350, 200, 100, "Resume Game")
        self.potion_button = Button(1000, 0, 200, 100, "Use Potion")

        self.game_engine = GameEngine()
        self.hero_position = Vector2d(0, 0)

    def run(self):
        weapon = Weapon("Sword", "A sharp blade", 10, 5, [Vector2d(0, 1),
                                                          Vector2d(1, 1), Vector2d(-1, 1), Vector2d(0, 2)])
        armor = Armor("Shield", "A sturdy shield", 15, 3)
        position = Vector2d(0, 0)
        list_of_moves = []
        max_health = 100
        direction = Directions.SOUTH
        self.create_character("Hero", 1, weapon, armor, position, list_of_moves, max_health, direction)
        self.game_engine.map.add_entity(self.hero)
        healing_potion = HealingPotion("Healing Potion", "A potion that heals you", 10, 5)
        mana_potion = ManaPotion("Mana Potion", "A potion that restores mana", 10, 5)
        self.hero.add_item(healing_potion)
        self.hero.add_item(mana_potion)
        self.hero.add_item(healing_potion)
        self.hero.add_item(mana_potion)
        self.hero.inventory.append(weapon)
        self.hero.inventory.append(armor)

        trap = Trap(1, Vector2d(2, 2), [], 10, Directions.NORTH, weapon)
        self.game_engine.map.add_entity(trap)
        self.traps.append(trap)

        weapon = Weapon("Claws", "Sharp claws", 10, 5, [Vector2d(0, 1), Vector2d(1, 1),
                                                        Vector2d(-1, 1), Vector2d(0, 2)])
        # enemy_position = Vector2d(0, 2)
        # enemy_list_of_moves = [Directions.NORTH]
        # enemy_max_health = 20
        # enemy_direction = Directions.SOUTH
        # enemy = Enemy(1, enemy_position, enemy_list_of_moves, enemy_max_health, enemy_direction, weapon)
        # self.game_engine.map.add_entity(enemy)
        # self.enemies.append(enemy)

        self.place_enemies(15)

        self.equip_weapon(weapon)
        self.equip_armor(armor)

        self.set_offset()

        while self.running:
            self.handle_events()
            self.draw()
            self.update()
            self.clock.tick(60)
            sleep(0.01)
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
                potions_per_row = 2
                potion_width, potion_height = 100, 50
                start_x, start_y = 1000, 250
                for i, item in enumerate(self.hero.inventory):
                    if isinstance(item, HealingPotion) or isinstance(item, ManaPotion):
                        row = i // potions_per_row
                        col = i % potions_per_row
                        x = start_x + col * potion_width
                        y = start_y + row * potion_height
                        potion_rect = pygame.Rect(x, y, potion_width, potion_height)
                        if potion_rect.collidepoint(mouse_pos):
                            print(f"Potion {i} clicked")
                            self.selected_potion_index = i
                            return
                weapons = [item for item in self.hero.inventory if isinstance(item, Weapon)]
                armors = [item for item in self.hero.inventory if isinstance(item, Armor)]

                equipment_per_row = 2
                equipment_width, equipment_height = 100, 50
                start_x, start_y = 1000, 400
                for i, item in enumerate(weapons):
                    row = i // equipment_per_row
                    col = i % equipment_per_row
                    x = start_x + col * equipment_width
                    y = start_y + row * equipment_height
                    equipment_rect = pygame.Rect(x, y, equipment_width, equipment_height)
                    if equipment_rect.collidepoint(mouse_pos):
                        print(f"Weapon {i} clicked")
                        self.selected_equipment_index = i
                        return
                for i, item in enumerate(armors):
                    row = (i + len(weapons)) // equipment_per_row
                    col = (i + len(weapons)) % equipment_per_row
                    x = start_x + col * equipment_width
                    y = start_y + row * equipment_height
                    equipment_rect = pygame.Rect(x, y, equipment_width, equipment_height)
                    if equipment_rect.collidepoint(mouse_pos):
                        print(f"Armor {i + len(weapons)} clicked")
                        self.selected_equipment_index = i + len(weapons)
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
                    self.hero.position = Vector2d(0, 0)
                    self.hero.current_direction = Directions.SOUTH
                    for enemy in self.enemies:
                        enemy.position = Vector2d(0, 2)
                        self.game_engine.map.add_entity(enemy)
                    for trap in self.traps:
                        trap.position = Vector2d(2, 2)
                        self.game_engine.map.add_entity(trap)
                    self.game_engine.map.add_entity(self.hero)
                    self.deck.generate_cards(5)
                    self.set_offset()
                elif self.resume_button.is_clicked(event):
                    self.paused = False
                elif self.potion_button.is_clicked(event):
                    if self.selected_potion_index is not None:
                        selected_potion = self.hero.inventory[self.selected_potion_index]
                        self.use_potion(selected_potion)
                        self.selected_potion_index = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.move_counter = 0
                    self.hero.list_of_moves = [Directions.SOUTH] * 5
                    for enemy in self.enemies:
                        enemy.list_of_moves = [Directions.NORTH] * 5
                elif event.key == pygame.K_UP:
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
        self.offset_y = screen_center_y - hero_global_y

    def update(self):
        if self.hero.list_of_moves:
            self.game_engine.map.perform_turn()
            self.move_counter += 1
            if self.move_counter == 5:
                self.hero.list_of_moves = []
        for enemy in self.enemies:
            if enemy.list_of_moves:
                enemy.list_of_moves.pop(0)
        self.set_offset()

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
        else:
            self.draw_map()
            self.draw_cards()
            self.draw_potions()
            self.draw_equipment()
            self.draw_character_info()
            self.pause_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.reset_button.draw(self.screen)
            self.potion_button.draw(self.screen)
        pygame.display.flip()

    def draw_map(self):
        map = self.game_engine.map
        scale = 3

        pygame.display.flip()

        for tile_position, tile in map.tiles_dictionary.items():
            for cell_position, cell in tile.cells_dict.items():
                min_x, max_x, min_y, max_y = self.game_engine.map.map_dimensions()
                print(min_x, max_x, min_y, max_y)
                cells_in_tile = self.game_engine.map.cells_in_tile
                global_x, global_y = tile_position.x * cells_in_tile + cell_position.x, tile_position.y * cells_in_tile + cell_position.y
                x, y = (global_x + self.offset_x) / scale, (global_y + self.offset_y) / scale
                if cell.wall.type == WallType.FULL or (not (min_x <= global_x <= max_x + map.cells_in_tile) or not (min_y <= global_y <= max_y + map.cells_in_tile )):
                    self.screen.blit(
                        pygame.transform.scale(self.wall_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                elif cell.wall.type == WallType.HALF:
                    image = self.images[cell.wall.type][cell.wall.facing]
                    self.screen.blit(
                        pygame.transform.scale(self.floor_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                    self.screen.blit(
                        pygame.transform.scale(image, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                elif cell.wall.type == WallType.EMPTY:
                    self.screen.blit(
                        pygame.transform.scale(self.floor_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                if any(isinstance(entity, Skel) for entity in cell.entities):
                    self.screen.blit(
                        pygame.transform.scale(self.skeleton_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                if any(isinstance(entity, Hero) for entity in cell.entities):
                    arrow_x = x
                    arrow_y = y
                    if self.hero.current_direction == Directions.NORTH:
                        arrow_y -= 1
                        image_rotated = pygame.transform.rotate(self.red_arrow_texture, 90)
                        self.screen.blit(
                            pygame.transform.scale(image_rotated, (self.scale // scale, self.scale // scale)),
                            (x * self.scale, y * self.scale))
                    elif self.hero.current_direction == Directions.SOUTH:
                        arrow_y += 1
                        image_rotated = pygame.transform.rotate(self.red_arrow_texture, 270)
                        self.screen.blit(
                            pygame.transform.scale(image_rotated, (self.scale // scale, self.scale // scale)),
                            (x * self.scale, y * self.scale))
                    elif self.hero.current_direction == Directions.WEST:
                        arrow_x -= 1
                        image_rotated = pygame.transform.rotate(self.red_arrow_texture, 180)
                        self.screen.blit(
                            pygame.transform.scale(image_rotated, (self.scale // scale, self.scale // scale)),
                            (x * self.scale, y * self.scale))
                    elif self.hero.current_direction == Directions.EAST:
                        arrow_x += 1
                        image_rotated = pygame.transform.rotate(self.red_arrow_texture, 0)
                        self.screen.blit(
                            pygame.transform.scale(image_rotated, (self.scale // scale, self.scale // scale)),
                            (x * self.scale, y * self.scale))
                    self.screen.blit(
                        pygame.transform.scale(self.hero_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                if any(isinstance(entity, Enemy) for entity in cell.entities):
                    self.screen.blit(
                        pygame.transform.scale(self.enemy_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))
                if any(isinstance(entity, Trap) for entity in cell.entities):
                    self.screen.blit(
                        pygame.transform.scale(self.trap_texture, (self.scale // scale, self.scale // scale)),
                        (x * self.scale, y * self.scale))

    def draw_character_info(self):
        font = pygame.font.Font(None, 36)

        hp_text = font.render(f"HP: {self.hero.current_health}", True, (255, 255, 255))
        gold_text = font.render(f"Gold: {self.hero.money}", True, (255, 255, 255))
        position_text = font.render(f"Position: {self.hero.position}", True, (255, 255, 255))

        text_x = self.window_rex_x - 200
        hp_text_y = self.window_rex_y - 100
        gold_text_y = self.window_rex_y - 70
        position_text_y = self.window_rex_y - 40

        self.screen.blit(hp_text, (text_x, hp_text_y))
        self.screen.blit(gold_text, (text_x, gold_text_y))
        self.screen.blit(position_text, (text_x, position_text_y))

    def place_enemies(self, num_enemies):
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
                enemy = Enemy(1, position, enemy_list_of_moves, enemy_max_health, enemy_direction, weapon)
                self.game_engine.map.add_entity(enemy)
                print(f"Enemy placed at {position}")
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
                image = self.images[card.wall.type][card.wall.facing]
                scaled_image = pygame.transform.scale(image, (card_width, card_height))
                if i == self.selected_card_index:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x, y, card_width, card_height), 3)
                self.screen.blit(scaled_image, (x, y))

    def draw_potions(self):
        potions_per_row = 2
        potion_width, potion_height = 100, 50
        start_x, start_y = 1000, 250

        for i, item in enumerate(self.hero.inventory):
            row = i // potions_per_row
            col = i % potions_per_row
            x = start_x + col * potion_width
            y = start_y + row * potion_height
            if isinstance(item, HealingPotion):
                scaled_image = pygame.transform.scale(self.healing_potion_texture, (potion_width, potion_height))
                self.screen.blit(scaled_image, (x, y))
            if isinstance(item, ManaPotion):
                scaled_image = pygame.transform.scale(self.mana_potion_texture, (potion_width, potion_height))
                self.screen.blit(scaled_image, (x, y))
            if i == self.selected_potion_index:
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, potion_width, potion_height), 3)

    def draw_equipment(self):
        equipment_per_row = 2
        equipment_width, equipment_height = 100, 50
        start_x, start_y = 1000, 400

        weapons = [item for item in self.hero.inventory if isinstance(item, Weapon)]
        armors = [item for item in self.hero.inventory if isinstance(item, Armor)]

        for i, item in enumerate(weapons):
            row = i // equipment_per_row
            col = i % equipment_per_row
            x = start_x + col * equipment_width
            y = start_y + row * equipment_height
            scaled_image = pygame.transform.scale(self.sword_texture, (equipment_width, equipment_height))
            self.screen.blit(scaled_image, (x, y))
            if i == self.selected_equipment_index:
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, equipment_width, equipment_height), 3)

        for i, item in enumerate(armors):
            row = (i + len(weapons)) // equipment_per_row
            col = (i + len(weapons)) % equipment_per_row
            x = start_x + col * equipment_width
            y = start_y + row * equipment_height
            scaled_image = pygame.transform.scale(self.armour_texture, (equipment_width, equipment_height))
            self.screen.blit(scaled_image, (x, y))
            if i + len(weapons) == self.selected_equipment_index:
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, equipment_width, equipment_height), 3)


if __name__ == "__main__":
    game = Game()
    game.run()