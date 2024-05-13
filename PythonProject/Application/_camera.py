import pygame

class Camera:
    def __init__(self, position):
        self.position = position

    def update(self, hero_position):
        self.position = hero_position
    # TODO: Implement the Camera class