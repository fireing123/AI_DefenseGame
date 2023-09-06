from typing import Any, Dict
import pygame
#not import my module
from object import GameObject

ground_group = pygame.sprite.Group()

class Ground(GameObject):
    
    def __init__(self, position, scale):
        super().__init__("ground", 2)
        ground_group.add(self)
        self.image = pygame.Surface(scale)
        self.rect = self.image.get_rect()
        self.position = position

    @staticmethod
    def instantiate(json: Dict):
        return Ground(
            json['position'],
            json['scale']
        )