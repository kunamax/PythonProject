import pygame

class Text:
    def __init__(self, x, y, text, color=(50, 50, 50)):
        self.position = (x, y)
        self.text = text
        self.color = color

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.color)
        screen.blit(text, self.position)