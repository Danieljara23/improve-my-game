import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK, RED
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
        self.health = 100  # Salud del jugador
        self.max_health = 100  # Salud máxima
        self.score = 0  # Puntuación del jugador
        self.score_increment = 1  # Incremento de puntuación por segundo

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

        for obstacle in self.obstacles:
            obstacle.update()

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.health -= 25  # Resta salud al chocar con un obstáculo
                self.obstacles.remove(obstacle)  # Elimina el obstáculo al chocar
                if self.health <= 0:
                    self.draw_text("¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

        # Incrementar la puntuación
        self.score += self.score_increment / FPS  # Aumentar la puntuación de acuerdo al tiempo

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Dibujar la barra de salud en la pantalla
        self.draw_health_bar(self.health, self.max_health)

        # Dibujar la puntuación en la pantalla
        self.draw_text(f"Puntuación: {int(self.score)}", font, BLACK, self.screen, WIDTH // 2, 50)

    def draw_health_bar(self, health, max_health):
        bar_length = 200
        bar_height = 20
        fill = (health / max_health) * bar_length
        pygame.draw.rect(self.screen, (255, 0, 0), (50, 50, bar_length, bar_height))  # Fondo de la barra
        pygame.draw.rect(self.screen, (0, 255, 0), (50, 50, fill, bar_height))  # Salud actual

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

