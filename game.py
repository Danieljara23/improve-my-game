import pygame
import random
import sys
from config import HEIGHT, FPS, RED, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")
        
        
        self.font = pygame.font.Font(None, 36)
        self.score_font = pygame.font.Font(None, 48)

       
        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2
        
        
        self.score = 0
        self.lives = 3  
        self.health = 100  
        self.max_health = 100
        self.collision_count = 0
        self.max_collisions = 3

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        
                        self.score += 10  

            
            self.update()
            self.draw()
            self.show_score(10, 10)
            self.show_health(10, 50)
            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()

        
        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        self.score += 1

        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        player_rect = self.player.get_rect()

        for obstacle in self.obstacles:
            obstacle.update()

            if player_rect.colliderect(obstacle.rect):
                self.collision_count += 1
                self.health -= 25  

                self.obstacles.remove(obstacle)

                if self.health <= 0:
                    self.lives -= 1
                    self.health = self.max_health
                    if self.lives <= 0:
                        self.show_game_over()
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

        self.draw_text(f"Colisiones: {self.collision_count}", self.font, BLACK, self.screen, 100, 300)

        self.draw_text(f"Vidas: {self.lives}", self.font, BLACK, self.screen, WIDTH - 100, 30)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def show_score(self, x, y):
        score_text = self.score_font.render("Puntuación: " + str(self.score), True, BLACK)
        self.screen.blit(score_text, (x, y))

    def show_health(self, x, y):
        health_text = self.font.render("Salud:", True, BLACK)
        self.screen.blit(health_text, (x+20, y+40))
        
        health_color = (255 - (255 * self.health // self.max_health), 
                        255 * self.health // self.max_health, 0)
        pygame.draw.rect(self.screen, health_color, (x+100, y+43, self.health, 20))

    def show_game_over(self):
        self.screen.fill(RED)
        game_over_text = self.font.render("¡GAME OVER!", True, BLACK)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000) 
