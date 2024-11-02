import pygame
from config import RED


class Obstacle:
    def __init__(self, x, y,speed):
        self.rect = pygame.Rect(x, y , 50, 50)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
