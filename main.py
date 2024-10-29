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

    # Bucle principal del juego
    running = True
    while running:
        game.menu(game.death_count)  # Mostrar el menú
        game.death_count = 0  # Reiniciar el contador de muertes al iniciar

        # Bucle de juego
        while running:
            game.update()
            game.draw()
            pygame.display.flip()
            
            # Eventos para cerrar el juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            game.clock.tick(FPS)  # Control de FPS

    pygame.quit()
    sys.exit()