import pygame
from typing import Dict
from pygame.sprite import Group
from pygame import Surface
from object import LivingObject
from weapon import shot_group, EnemyShot
from event import enemy_death

enemy_group = Group()

class Enemy(LivingObject):
    """
    """
    def __init__(self, name, position, xml_path):
        super().__init__(name, position, xml_path)
        self.exp_ponit = 50
        enemy_group.add(self)
    
    def update(self, mod):
        super().update(mod)
        collision = pygame.sprite.spritecollide(self, shot_group, True)
        for collide in collision:
            self.hp -= collide.power
            collide.delete()
        
    def attack(self, player):
        pass
    
    def delete(self):
        enemy_death.invoke(self.exp_ponit)
        super().delete()


class Soldier(Enemy):
    """
    적군인 오브젝트 전진, 발사기능이 있음
    """
    
    def __init__(self, name, position):
        super().__init__(name, position, 'src/image/soldier/config.xml')
        self.hp = 100
        self.max_hp = 100
        self.speed = 2
        self.tick = 200
        self.last_update = 0
        
    def update(self, mod):
        super().update(mod)
        
        
        
        collision = pygame.sprite.spritecollide(self, shot_group, False)
        
        for collide in collision:
            self.hp -= collide.power
            collide.remove()
    
    def attack(self, player):
        if pygame.time.get_ticks() - self.last_update > self.tick:
            self.last_update = pygame.time.get_ticks()
            angle = self.look_angle(player.position)
            EnemyShot("ew", self.position, angle * 5)

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