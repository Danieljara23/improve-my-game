import pygame
from utils import load_spritesheet
from config import HEIGHT


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 150
        self.speed = 2
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.run_frames=[]
        self.jump_frames = []
        self.damage_frames=[]
        self.is_damaged = False
        self.damage_duration = 30  # Duración de la animación de daño en frames
        self.damage_counter = 0

        for num in range (1,8):
            img_run=pygame.image.load(f"assets/player1/run/Character2F_1_run_{num}.png")
            img_run =pygame.transform.scale(img_run, (self.width,self.height))
            self.run_frames.append(img_run)

        for num2 in range (1,3):
            img_jump=pygame.image.load(f"assets/player1/jump/Character2F_1_jump_{num2}.png")
            img_jump =pygame.transform.scale(img_jump, (self.width,self.height))
            self.jump_frames.append(img_jump)

        for num3 in range(1,2):
            
            img_damage=pygame.image.load(f"assets/player1/damage/Character2F_1_damage_{num3}.png")
            img_damage =pygame.transform.scale(img_damage, (self.width,self.height))
            self.damage_frames.append(img_damage)

        
       
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
        
        if self.is_damaged:
            self.damage_counter += 1
            if self.damage_counter >= self.damage_duration:
                self.is_damaged = False
                self.damage_counter = 0
    
    
    def take_damage(self):
        # Activa la animación de daño aquí
        # Luego, una vez que termine la animación, resetea `is_damaged`:
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Temporizador de 500 ms

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.is_damaged = False


    def draw(self, surface):

        if self.is_damaged:
            frame = self.damage_frames[0]  # Mostrar el primer (y único) frame de daño
        elif self.on_ground:
            # Animación de correr
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.run_frames):
                self.frame_index = 0
            frame = self.run_frames[int(self.frame_index)]
        else:
            # Animación de salto
            frame = self.jump_frames[0]

        surface.blit(frame, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(
            self.x + (self.width - self.hitbox_width) // 2,
            self.y + (self.height - self.hitbox_height) // 2,
            self.hitbox_width,
            self.hitbox_height
        )
