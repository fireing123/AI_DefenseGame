from typing import Dict
import pygame
from object import GameObject

group = pygame.sprite.Group()

class Ground(GameObject):
    
    def __init__(self, position, scale):
        super().__init__("ground")
        group.add(self)
        self.image = pygame.Surface(scale)
        self.rect = self.image.get_rect()
        self.rect.center = position
        
    def render(self, surface):
        surface.blit(self.image, self.rect)
        
    @staticmethod
    def instantiate(json: Dict):
        return Ground(
            json['position'],
            json['scale']
        )