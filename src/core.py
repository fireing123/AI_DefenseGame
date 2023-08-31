from typing import Dict
import pygame
import manger
from object import GameObject
from weapon import shot_group
class Core(GameObject):
    
    def __init__(self, name: str, hp, position):
        super().__init__(name)
        self.hp = hp
        self.max_hp = hp
        self.image = pygame.image.load('src/image/core.png')
        self.rect = self.image.get_rect()
        self.position = position
        
        self.hp_bar = manger.HPbar(name+"hpBar", self)
        
    def update(self):
        super().update()
        
        collision = pygame.sprite.spritecollide(self, shot_group, True)
        
        for collide in collision:
            self.hp -= collide.power
            collide.remove()
        
        if self.hp < 0:
            self.world.is_running = False
            
            
    def set_world(self, world):
        self.world = world
        
    @staticmethod
    def instantiate(json: Dict):
        return Core(
            json['name'],
            100,
            json['position']
        )