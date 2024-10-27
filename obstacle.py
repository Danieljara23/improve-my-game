import pygame
from config import RED


class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 500)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
