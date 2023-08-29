import pygame
import math
from typing import Dict, List
#not import my module
import manger
from object import LivingObject
from camera import camera
#import module first
from weapon import Shot, enemy_shot_group
from enemy import enemy_group, Enemy


class Player(LivingObject):
    
    
    
    def __init__(self, name: str, position):
        super().__init__(name, position, 'src/image/ai/config.xml')
        self.keys = {}
        get_width, get_height = manger.screen.get_size()
        self.width, self.height = get_width/2, get_height/2
        self.health = 100
        self.speed = 2
        self.jump_speed = -6
        self.mass = True
        self.on_ground = True
        self.tick = 200
        self.last_update = 0
        
        
    def player_event(self, event : pygame.event.Event):
        
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
            if event.key == pygame.K_UP and self.on_ground:
                self.jump()
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False
    
    def update(self):  

        if self.keys.get(pygame.K_RIGHT):
            self.direction.x = self.speed
        if self.keys.get(pygame.K_LEFT):
            self.direction.x = -self.speed
        if self.keys.get(pygame.K_0): 
            if pygame.time.get_ticks() - self.last_update > self.tick:
                self.last_update = pygame.time.get_ticks()
                sx, sy = self.position
                sped = math.copysign(1, self.direction.x)
                Shot("shot", (sx, sy-50), pygame.Vector2(50 * sped , 5))

        super().update()

        for enemy in enemy_group.sprites():
            if self.recognition_range.colliderect(enemy.rect):
                enemy.attack(self)
                
        collision = pygame.sprite.spritecollide(self, enemy_shot_group, False)
        
        for collide in collision:
            self.hp -= collide.power
            collide.remove()
            
            
        if self.rect_position[0] > self.width * 0.85:
            camera.x += 1

        if self.rect_position[0] < self.width * 0.25:
            camera.x -= 1

        #animation 
        self.image = self.animation_controller.update()
    
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def jump(self):
        self.add_force(0, self.jump_speed)
        self.on_ground = False
    
    @staticmethod
    def instantiate(json: Dict):
        return Player("super", json['position'])