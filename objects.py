import pygame
from config import RED


class LifeObject:
    def __init__(self, x, y, speed,image):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = speed
        self.image=image

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
