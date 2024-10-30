import pygame
from config import RED


class LifeObject:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 100)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,0), self.rect)
