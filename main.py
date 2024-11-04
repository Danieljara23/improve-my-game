import pygame

from game import Game
from config import WIDTH, HEIGHT

# Inicializar Pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speedrunner")

if __name__ == "__main__":
    game = Game()
    game.run()  