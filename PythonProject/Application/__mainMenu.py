from ._button import Button
import pygame


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.new_game_button = Button(500, 350, 200, 100, "New Game")
        self.resume_button = Button(500, 200, 200, 100, "Resume")
        self.quit_button = Button(500, 500, 200, 100, "Quit")

    def draw(self):
        self.new_game_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pygame.display.flip()

    def draw_pause(self):
        self.resume_button.draw(self.screen)
        self.new_game_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pygame.display.flip()

    def handle_events(self, event)->int:
        if self.resume_button.is_clicked(event):
            return 2
        if self.new_game_button.is_clicked(event):
            return 1
        if self.quit_button.is_clicked(event):
            return -1
        return 0
