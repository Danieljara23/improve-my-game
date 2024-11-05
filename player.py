import pygame
from utils import load_spritesheet
from config import HEIGHT


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.lives = 3  # Inicializa las vidas
        self.run_frames = load_spritesheet(
            "assets/player/run.png", self.width, self.height
        )
        self.jump_frames = load_spritesheet(
            "assets/player/jump.png", self.width, self.height
        )

        self.frame_index = 0
        self.animation_speed = 0.3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        self.velocity_y += self.gravity
        self.y += self.velocity_y
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, surface):
        if self.on_ground:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.run_frames):
                self.frame_index = 0
            frame = self.run_frames[int(self.frame_index)]
        else:
            frame = self.jump_frames[0]
        surface.blit(frame, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_health_lives(self, screen, font):
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 70))
