import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK, RED
from player import Player
from obstacle import Obstacle
from utils import load_spritesheet

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
        self.collision_count = 0
        self.max_collisions = 3
        self.width = 32
        self.height = 32
    # Tiempo inicio puntaje
# ------------------------------
        self.start_time = pygame.time.get_ticks()  
        self.score = 0 
# ------------------------------
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

# ----------------------
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  
        self.score = int(elapsed_time)  
# ----------------------

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
    # Daño recibido
# -----------------------------------
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.collision_count += 1
                self.obstacles.remove(obstacle)

                parpadeo_inicio = pygame.time.get_ticks()
                parpadeando = True
                while parpadeando:
                    current_time = pygame.time.get_ticks()
                    if (current_time - parpadeo_inicio) % 500 < 250:
                        pygame.draw.rect(self.screen, (RED), player_rect)
                    else:
                        self.player.draw(self.screen)
                    pygame.display.flip()
                    if (current_time - parpadeo_inicio) > 1000:  
                        parpadeando = False
# ------------------------------------
        if self.collision_count >= self.max_collisions:
            self.draw_text(
                        "¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                         ) 
            pygame.time.wait(2000)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.draw_text(
            f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30
        )
# -------
        self.draw_text(f"  Puntuación: {self.score}", font, BLACK, self.screen, 100, 60)
# -------
        self.draw_text(f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30)


    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
