import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import *
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
        self.background_image = pygame.image.load("assets/background/background.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.background_image2 = pygame.image.load("assets/background/background2.png").convert_alpha()
        self.background_image2 = pygame.transform.scale(self.background_image2, (WIDTH, HEIGHT))
        self.background_image3 = pygame.image.load("assets/background/background3.png").convert_alpha()
        self.background_image3 = pygame.transform.scale(self.background_image3, (WIDTH, HEIGHT))
        # self.ground = pygame.image.load("assets/suelo.png").convert_alpha()
        # self.ground = pygame.transform.scale(self.ground,(700,150))
        self.background_scroll = 0
        self.background_speed = 4
        self.collision_count = 0
        self.max_collisions = 3
        self.death_count = 0
        self.is_damaged=False
        self.points=0
      

    def menu(self,death_count):
        waiting = True
        while waiting:
            self.screen.fill(WHITE)

            if death_count == 0:
                text = self.draw_text(
                    "¡Bienvenido a Speedrunner! Presiona cualquier tecla para comenzar",
                    font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                )
            else:
                text = self.draw_text(
                    "¡Perdiste! Presiona cualquier tecla para intentarlo de nuevo",
                    font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                )
                score = self.draw_text(
                    f"Puntuación: {self.points}", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 + 50
                )

            pygame.display.flip()  # Solo actualiza el menú en pantalla

            # Espera hasta que el jugador presione una tecla para salir del menú
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
            
            self.clock.tick(FPS)

    def update(self):
        self.player.update()

        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 70
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
                self.player.take_damage()
                self.collision_count += 1
                pygame.time.delay(500)
                self.obstacles.remove(obstacle)

                if self.collision_count >= self.max_collisions:
                    self.death_count+=1
                    self.menu(self.death_count)
                    self.collision_count = 0
                    self.points = 0
                    pygame.time.wait(2000)
                    return
        else:
            self.score()
        
    def take_damage(self):
        # """Función para aplicar el daño al jugador."""
        if not self.is_damaged:
            self.is_damaged = True
            self.player.take_damage()  # Llama a la animación de daño del jugador
            print("Player has taken damage!") 

    
    
    def score(self):
        self.points += 1
        if self.points % 200 == 0:
            self.background_speed += 1
            print("Speed increased!")
            print(f"Speed: {self.background_speed}")

            

    def draw(self):
        
        self.screen.blit(self.background_image3, (0, 0))
        self.screen.blit(self.background_image2, (self.background_scroll , 0))
        self.screen.blit(self.background_image2,(self.background_scroll + self.background_image2.get_width(), 0),)
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(self.background_image,(self.background_scroll + self.background_image.get_width(), 0),)
        
        # self.screen.blit(self.ground, (-200,350))  # Ajusta la altura para el suelo
        # self.screen.blit(self.ground, (self.background_scroll + self.ground.get_width(), 350))

        self.player.draw(self.screen)


        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.draw_text(
            f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30
        )
        self.draw_text(
            f"Puntos: {self.points}", font, BLACK, self.screen, 100, 60
        )

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
