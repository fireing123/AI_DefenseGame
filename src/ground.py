import os
from typing import Any, Dict
import pygame
#not import my module
from object import GameObject

ground_group = pygame.sprite.Group()

class Ground(GameObject):
    
    def __init__(self, position, scale, image):
        super().__init__("ground", 2)
        ground_group.add(self)
        self.ground_image = pygame.image.load(os.getcwd()+"/"+image)
        self.image = pygame.Surface(scale)
        self.rect = self.image.get_rect()
        self.position = position
        for i in range(self.rect.size[0] // self.ground_image.get_rect().size[0]):
            self.image.blit(self.ground_image, [i * self.ground_image.get_rect().size[0], 0])

    @staticmethod
    def instantiate(json: Dict):
        return Ground(
            json['position'],
            json['scale'],
            json['path']
        )