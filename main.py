import pygame

from game import *
from config import WIDTH, HEIGHT

# Inicializar Pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speedrunner")

if __name__ == "__main__":
    game = Game()
    game.death_count = 0 

    running = True
    while running:
        game.menu(game.death_count)  # Mostrar el menú
        game.death_count = 0  

    
        while running:
            game.update()
            game.draw()
            pygame.display.flip()
            
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            game.clock.tick(FPS)  

    pygame.quit()
    sys.exit()