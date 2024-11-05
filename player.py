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
        self.run_frames = load_spritesheet(
            "assets/player/run.png", self.width, self.height
        )
        self.jump_frames = load_spritesheet(
            "assets/player/jump.png", self.width, self.height
        )

        self.frame_index = 0
        self.animation_speed = 0.3
        

        # Se incluye la variable de salud en la interfaz
        self.max_health = 3
        self.current_health = self.max_health
        self.heart_image = pygame.image.load("assets/heart_asset.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (24, 24))

    # Definir método para reducir la salud
    def damage(self):
        self.current_health -= 1
        return self.current_health <= 0
    
    # Definir método para "curarse"
    def heal(self):
        if self.current_health < self.max_health:
            self.current_health += 1
            return True
        return False
    
    # Se dibuja la salud en la interfaz
    def draw_health(self, surface):
        for i in range(self.current_health):
            surface.blit(self.heart_image, (10 + i * 30, 10))

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
