import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

# Se importó la clase Health del archivo health.py
from health import Health

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

        # Variables para la generación de corazones y duración de invulnerabilidad
        self.last_collision_time = 0
        self.invulnerability_duration = 1000
        self.hearts = []
        self.last_heart_spawn_time = pygame.time.get_ticks()
        self.heart_spawn_interval = random.randint(2000, 5000)
        
        # Variables de puntuación
        self.score = 0
        self.obstacle_points = 1

        # Variables para el parpadeo
        self.blink_interval = 100  # Intervalo de parpadeo en milisegundos
        self.is_visible = True

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

    # Pygame recibe el tiempo en milisegundos
    def update(self):
        current_time = pygame.time.get_ticks()
        self.player.update()

        # Actualizar estado de parpadeo durante invulnerabilidad
        if current_time - self.last_collision_time <= self.invulnerability_duration:
            if (current_time // self.blink_interval) % 2 == 0:
                self.is_visible = True
            else:
                self.is_visible = False
        else:
            self.is_visible = True

        # Generación de corazones a intervalos aleatorios
        if current_time - self.last_heart_spawn_time >= self.heart_spawn_interval:
            heart_x = WIDTH
            heart_y = random.randint(HEIGHT - 200, HEIGHT - 50)
            new_heart = Health(heart_x, heart_y)
            self.hearts.append(new_heart)
            self.last_heart_spawn_time = current_time
            self.heart_spawn_interval = random.randint(2000, 5000)

        # Actualizar corazones
        for heart in self.hearts[:]:
            heart.update()
            player_rect = self.player.get_rect()
            if player_rect.colliderect(heart.rect):
                self.player.heal()
                self.hearts.remove(heart)
            elif heart.rect.right < 0:
                self.hearts.remove(heart)

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

        # Sistema de puntuación por obstáculo evitado
        player_x = self.player.x
        for obstacle in self.obstacles:
            if obstacle.rect.right < player_x and obstacle.rect.right + obstacle.speed >= player_x:
                self.score += self.obstacle_points
                
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                # Si el jugador no es invulnerable, se hace daño
                if current_time - self.last_collision_time > self.invulnerability_duration:
                    self.last_collision_time = current_time
                    self.player.damage()
                    if self.player.current_health <= 0:
                        self.obstacles.remove(obstacle)
                        self.draw_game_over()

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        # Muestra las vidas en la esquina superior izquierda
        self.player.draw_health(self.screen)

        # Dibuja los corazones disponibles en la lista
        for heart in self.hearts:
            heart.draw_heart(self.screen)

        # Solo dibuja el jugador si is_visible es True
        if self.is_visible:
            self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Se muestra la puntuación
        self.draw_text(f"Puntuación: {self.score}", font, BLACK, self.screen, WIDTH - 150, 30)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)


    # Se define un método para cuando el jugador pierde
    def draw_game_over(self):
        self.screen.fill(WHITE)
        self.draw_text("¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 - 50)
        self.draw_text(f"Puntuación: {self.score}", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()