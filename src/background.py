import pygame
from object import GameObject
import color
# 교체 해야함.

class BlcakRectangle(pygame.sprite.Sprite):
    def __init__(self, size, coordinate):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color.BLACK)
        self.rect = self.image.get_rect()
        self.rect.topright = coordinate

class BackGround(GameObject):
    def __init__(self, size, path):
        super().__init__(0)
        self.image = pygame.image.load(path)
        self.size = size
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        
    def update(self):
        self.rect = self.image.get_rect()
        
    def change_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
    
    def render(self, surface):
        surface.blit(self.image, self.rect)