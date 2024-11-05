import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.init()
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
        
        # Propiedades de la barra de vida
        self.max_health = 100
        self.current_health = self.max_health
        self.health_bar_length = 200
        self.health_bar_height = 20
        self.health_ratio = self.max_health / self.health_bar_length
        
        # Propiedades de la puntuación
        self.score = 0
        self.score_speed = 1  # Velocidad de incremento de la puntuación
        
    def draw_health_bar(self):
        x, y = 20, 60
        
        # Barra roja (fondo)
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.health_bar_length, self.health_bar_height))
        
        # Barra verde (salud)
        if self.current_health > 0:
            current_health_width = int((self.current_health / self.max_health) * self.health_bar_length)
            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, current_health_width, self.health_bar_height))
        
        # Borde de la barra
        pygame.draw.rect(self.screen, BLACK, (x, y, self.health_bar_length, self.health_bar_height), 2)
            
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

        # Fondo en movimiento
        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        # Generar obstáculos
        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        # Actualizar obstáculos
        for obstacle in self.obstacles:
            obstacle.update()

        # Eliminar obstáculos fuera de la pantalla
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.rect.x + obstacle.rect.width > 0]

        # Verificar colisiones
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.collision_count += 1
                self.current_health -= self.max_health / self.max_collisions  # Reduce salud en 33.3333 puntos por colisión
                self.obstacles.remove(obstacle)
                
                if self.collision_count >= self.max_collisions or self.current_health <= 0:
                    self.draw_text(f"¡Perdiste! Puntuación: {self.score}", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.wait(4000)
                    pygame.quit()
                    sys.exit()

        # Actualizar puntuación
        self.score += self.score_speed

    def draw(self):
        # Dibujar fondo
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(self.background_image, (self.background_scroll + self.background_image.get_width(), 0))

        # Dibujar jugador y obstáculos
        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Dibujar texto de colisiones, puntuación y barra de salud
        self.draw_text(f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30)
        self.draw_text(f"Puntuación: {self.score}", font, BLACK, self.screen, WIDTH - 150, 30)
        self.draw_health_bar()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
