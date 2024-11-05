import pygame

# Se crea la clase Health
class Health:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.image = pygame.image.load("assets/heart_asset.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)

# Método para definir y actualizar las posiciones y desplazamiento de los corazones
    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

# Método para dibujar los corazones en la superficie
    def draw_heart(self, surface):
        surface.blit(self.image, (self.x, self.y))
  
