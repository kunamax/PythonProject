from ._button import Button
import pygame


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.new_game_button = Button(500, 350, 200, 100, "New Game")

    def draw(self):
        self.new_game_button.draw(self.screen)
        pygame.display.flip()

    def handle_events(self, event):
        if self.new_game_button.is_clicked(event):
            return True
        return False