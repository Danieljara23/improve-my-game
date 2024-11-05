import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2

        # Inicializar puntuación y vidas
        self.score = 0
        self.lives = 3

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()

        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        for obstacle in self.obstacles[:]:
            obstacle.update()

            # Chequeo de colisión
            if self.player.get_rect().colliderect(obstacle.rect):
                self.lives -= 1
                self.obstacles.remove(obstacle)
                if self.lives <= 0:
                    self.draw_text(
                        "¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                    )
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

            # Sumar puntuación si el obstáculo pasa sin colisionar
            if obstacle.rect.right < 0:
                self.score += 10  # Incrementar puntuación
                self.obstacles.remove(obstacle)

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Ajustar la posición de la puntuación y las vidas
        self.draw_text(f"Puntuación: {self.score}", font, BLACK, self.screen, 20, 20)  # Ajustado
        self.draw_text(f"Vidas: {self.lives}", font, BLACK, self.screen, WIDTH - 150, 20)  # Ajustado

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)  # Cambié a .topleft para posicionar correctamente
        surface.blit(textobj, textrect)
