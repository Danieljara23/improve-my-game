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
        self.hearts = []  # Lista para corazones recogibles
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2
        self.score = 0  # Inicializa el puntaje

        # Carga y ajusta la imagen del corazón
        self.heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (32, 32))  # Tamaño ajustado a 32x32 píxeles

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

        # Movimiento del fondo
        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        # Generación aleatoria de obstáculos
        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        # Generación aleatoria de corazones (probabilidad ajustada)
        if random.randint(0, 100) < 1:  # Cambia 1 para ajustar la probabilidad (1%).
            heart_x = WIDTH
            heart_y = random.randint(100, HEIGHT - 150)  # Ajusta la altura del corazón
            self.hearts.append((heart_x, heart_y))  # Almacena la posición del corazón como una tupla

        # Actualizar obstáculos
        for obstacle in self.obstacles:
            obstacle.update()

        # Actualizar corazones
        for i in range(len(self.hearts)):
            heart_x, heart_y = self.hearts[i]
            heart_x -= 5  # Mueve el corazón hacia la izquierda
            self.hearts[i] = (heart_x, heart_y)  # Actualiza la posición

        # Remover obstáculos que salen de la pantalla
        self.obstacles = [
            obstacle for obstacle in self.obstacles if obstacle.rect.x + obstacle.rect.width > 0
        ]

        # Remover corazones que salen de la pantalla
        self.hearts = [
            (heart_x, heart_y) for heart_x, heart_y in self.hearts if heart_x > 0
        ]

        # Colisión con obstáculos
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.player.lives -= 1  # Resta una vida al jugador
                self.obstacles.remove(obstacle)  # Remueve el obstáculo tras la colisión
                if self.player.lives <= 0:
                    self.draw_text("¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

        # Colisión con corazones
        for i in range(len(self.hearts)):
            heart_x, heart_y = self.hearts[i]
            heart_rect = pygame.Rect(heart_x, heart_y, 32, 32)  # Crea un rectángulo para el corazón
            if player_rect.colliderect(heart_rect):
                self.player.lives += 1  # Aumenta una vida al jugador
                del self.hearts[i]  # Remueve el corazón tras ser recogido
                break  # Sale del bucle para evitar problemas al modificar la lista

        # Aumenta el puntaje cada vez que el jugador evita un obstáculo
        self.score += 0.01  # Incrementa lentamente el puntaje

    def draw(self):
        # Dibujar fondo con desplazamiento
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(self.background_image, (self.background_scroll + self.background_image.get_width(), 0))

        # Dibujar jugador y obstáculos
        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Dibujar corazones en la esquina superior izquierda
        for i in range(self.player.lives):
            self.screen.blit(self.heart_image, (10 + i * 40, 10))

        # Dibujar corazones recogibles
        for heart_x, heart_y in self.hearts:
            self.screen.blit(self.heart_image, (heart_x, heart_y))

        # Calcular y dibujar el fondo semi-transparente adaptado al texto del puntaje
        score_text = f"Puntuación: {int(self.score)}"
        score_surface = font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 60 + self.heart_image.get_height())  # Debajo de los corazones

        # Dibujar fondo negro semi-transparente detrás del puntaje
        background_rect = pygame.Rect(score_rect.left - 5, score_rect.top - 5, score_rect.width + 10, score_rect.height + 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), background_rect)  # Fondo semi-transparente

        # Dibujar el texto del puntaje
        self.screen.blit(score_surface, score_rect)

    def draw_text(self, text, font, color, surface, x, y, outline_color=None):
        # Si se proporciona un color de contorno, renderiza el texto con un borde
        if outline_color:
            outline_text = font.render(text, True, outline_color)
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_rect = outline_text.get_rect(center=(x + dx, y + dy))
                surface.blit(outline_text, outline_rect)

        # Renderiza el texto principal
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)
