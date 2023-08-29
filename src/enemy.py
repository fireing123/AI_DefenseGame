import pygame
from typing import Dict
from pygame.sprite import Group
from pygame import Surface
from object import LivingObject
from weapon import shot_group

enemy_group = Group()

class Enemy(LivingObject):
    """
    """
    
    
    def update(self):
        super().update()
        collision = pygame.sprite.spritecollide(self, shot_group, True)
        for collide in collision:
            self.hp -= collide.power
            collide.remove()
        
    def attack(self, player):
        pass

    def attack_possible(self, player):
        pass
    
    def advance(self, player):
        pass

class Soldier(Enemy):
    """
    적군인 오브젝트 전진, 발사기능이 있음
    """
    
    def __init__(self, name, position):
        super().__init__(name, position, 'src/image/soldier/config.xml')
        self.hp = 100
        self.max_hp = 100
        self.speed = 2
        

    def advance(self, player):
        # player 쪽으로 가기
        pass
        
    def update(self):
        super().update()
    
    def render(self, surface: Surface, camera: tuple):
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(self.image, self.rect_position)
    
    @staticmethod
    def instantiate(json: Dict):
        return Soldier(
            json['name'],
            json['position']
        )