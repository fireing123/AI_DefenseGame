from .. import color
import pygame


class BlcakRectangle(pygame.sprite.Sprite):
    def __init__(self, size, coordinate):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color.BLACK)
        self.rect = self.image.get_rect()
        self.rect.topright = coordinate

class BackGround(pygame.sprite.Sprite):
    def __init__(self, size, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.size = size
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        
        
    def change_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()