import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import *
from obstacle import *
from objects import *

pygame.font.init()
font = pygame.font.SysFont("Times New Roman", 48)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.objects=[]
        self.background_image = pygame.image.load("assets/background/background.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.background_image2 = pygame.image.load("assets/background/background2.png").convert_alpha()
        self.background_image2 = pygame.transform.scale(self.background_image2, (WIDTH, HEIGHT))
        self.background_image3 = pygame.image.load("assets/background/background3.png").convert_alpha()
        self.background_image3 = pygame.transform.scale(self.background_image3, (WIDTH, HEIGHT))
        self.life = pygame.image.load("assets/descargar.png").convert_alpha()   
        self.life = pygame.transform.scale(self.life,(40,40))     
        self.background_scroll = 0
        self.background_speed = 6
        self.life_count = 3
        self.max_collisions = 3
        self.death_count = 0
        self.is_damaged=False
        self.points=0
        self.obstacle_timer = 0
        self.life_object_timer = 0
        self.obstacle_delay = random.randint(20, 100)


    def reset_game(self):
        self.life_count = 3
        self.points = 0
        self.background_speed = 4  
        self.obstacles.clear()  
        self.objects.clear()     
        self.background_scroll = 0
        self.player.reset_animation()
      

    def menu(self,death_count):
        waiting = True
        while waiting:
            self.screen.fill(WHITE)

            if death_count == 0:
                self.draw_text(
                    "¡Bienvenido a Speedrunner!",
                    font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 - 20
                )
                self.draw_text(
                    "Presiona cualquier tecla para comenzar",
                    font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 +40
                )
                
            else:
                self.draw_text(
                    "¡Perdiste!",
                    font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 - 30
                )
                self.draw_text(
                    "Presiona cualquier tecla para intentarlo de nuevo",
                    font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2+10
                )
                self.draw_text(
                    f"Puntuación: {self.points}", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 + 50
                )

            pygame.display.flip()  

            # Espera hasta que el jugador presione una tecla para salir del menú
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    self.reset_game()
            
            self.clock.tick(FPS)

    def update(self):
        self.player.update()

        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        self.obstacle_timer += 1
        self.life_object_timer += 1

        if self.obstacle_timer > self.obstacle_delay:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 100
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y, self.background_speed))
            self.obstacle_timer = 0
            self.obstacle_delay = random.randint(30, 100)
        
        if (self.life_object_timer > 100 and self.life_count <= 2 and self.points >= 300 and self.life_count <= 5):
            max_attempts = 10
            for _ in range(max_attempts):
                life_object_x = WIDTH
                life_object_y = HEIGHT - 100
                life_object_rect = pygame.Rect(life_object_x, life_object_y, 40, 40,)
                if not any(life_object_rect.colliderect(obstacle.rect) for obstacle in self.obstacles):
                    self.objects.append(LifeObject(life_object_x, life_object_y, self.background_speed, self.life))
                    self.life_object_timer = 0
                    break
      

        for obstacle in self.obstacles:
            obstacle.update()

        for life_object in self.objects:
            life_object.update()

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        self.objects = [
            life_object 
            for life_object in self.objects 
            if life_object.rect.x + life_object.rect.width > 0
        ]


        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.player.take_damage()
                self.life_count -= 1
                pygame.time.delay(100)
                self.obstacles.remove(obstacle)

                if self.life_count <= 0:
                    self.death_count+=1
                    pygame.time.wait(1000)
                    
                    self.menu(self.death_count)
                    return
        else:
            self.score()
        
        for life_object in self.objects:
            if player_rect.colliderect(life_object.rect):
                self.life_count += 1
                self.objects.remove(life_object)  # Eliminar el objeto de vida

    # Función para aplicar el daño al jugador.
    def take_damage(self):
        if not self.is_damaged:
            self.player.take_damage() 
            print("Player has taken damage!") 
  
    def score(self):
        self.points += 1
        if self.points % 200 == 0:
            self.background_speed += 1          

    def draw(self):
        
        self.screen.blit(self.background_image3, (0, 0))
        self.screen.blit(self.background_image2, (self.background_scroll , 0))
        self.screen.blit(self.background_image2,(self.background_scroll + self.background_image2.get_width(), 0),)
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(self.background_image,(self.background_scroll + self.background_image.get_width(), 0),)

        self.player.draw(self.screen)


        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for object in  self.objects:
            object.draw(self.screen)

        self.draw_text(
            f"Vidas: {self.life_count}", font, BLACK, self.screen, 100, 30
        )
        self.draw_text(
            f"Puntos: {self.points}", font, BLACK, self.screen, 130, 65
        )

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
