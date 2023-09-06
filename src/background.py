import pygame
import color
#not import my module


class BlcakRectangle(pygame.sprite.Sprite):
    """
    화면전환시 생기는 검은 박스입니다.
    """
    def __init__(self, scale : tuple[int, int], coordinate : tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface(scale)
        self.image.fill(color.BLACK)
        self.rect = self.image.get_rect()
        self.rect.topright = coordinate

from object import GameObject

class BackGround(GameObject):
    """
    background object
    """
    def __init__(self, center, path):
        super().__init__("background", 0)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.position = center
 
    def change_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
    
    def render(self, surface, camera):
        super().render(surface, camera)
        
    @staticmethod 
    def instantiate(json):
        return BackGround(json['position'], json['image'])