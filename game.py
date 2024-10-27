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
        self.background_image = pygame.image.load("assets/background.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.background_image2 = pygame.image.load("assets/background2.png").convert_alpha()
        self.background_image2 = pygame.transform.scale(self.background_image2, (WIDTH, HEIGHT))
        self.background_image3 = pygame.image.load("assets/background3.png").convert_alpha()
        self.background_image3 = pygame.transform.scale(self.background_image3, (WIDTH, HEIGHT))
        self.background_scroll = 0
        self.background_speed = 4
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
                self.collision_count += 1
                self.obstacles.remove(obstacle)
                if self.collision_count >= self.max_collisions:
                    self.draw_text(
                        "¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                    )
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

    def draw(self):
        
        self.screen.blit(self.background_image3, (0, 0))
        self.screen.blit(self.background_image2, (self.background_scroll , 0))
        self.screen.blit(self.background_image2,(self.background_scroll + self.background_image2.get_width(), 0),)
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(self.background_image,(self.background_scroll + self.background_image.get_width(), 0),)

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.draw_text(
            f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30
        )

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
