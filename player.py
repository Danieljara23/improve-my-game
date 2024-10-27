import pygame
from utils import load_spritesheet
from config import HEIGHT


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y-50
        self.width = 150
        self.height = 150
        self.speed = 5
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.run_frames=[]
        self.jump_frames = []
        self.damage_frames=[]

        for num in range (1,8):
            img_run=pygame.image.load(f"assets/player1/Character2F_1_run_{num}.png")
            img_run =pygame.transform.scale(img_run, (self.width,self.height))
            self.run_frames.append(img_run)

        for num2 in range (1,2):
            img_jump=pygame.image.load(f"assets/player1/Character2F_1_jump_{num2}.png")
            img_jump =pygame.transform.scale(img_jump, (self.width,self.height))
            self.jump_frames.append(img_jump)

        #

        
       
        self.hitbox_width = 50
        self.hitbox_height = 75

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
        return pygame.Rect(
            self.x + (self.width - self.hitbox_width) // 2,
            self.y + (self.height - self.hitbox_height) // 2,
            self.hitbox_width,
            self.hitbox_height
        )
