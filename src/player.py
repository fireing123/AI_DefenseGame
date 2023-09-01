import pygame
import math
from typing import Dict, List
#not import my module
import manger
from object import LivingObject
from camera import camera
#import module first
from weapon import AllyShot, enemy_shot_group, EnemyShot
from enemy import enemy_group
from ui import HPbar

class Player(LivingObject):
    

    
    def __init__(self, name: str, position):
        super().__init__(name, position, 'src/image/ai/config.xml')
        self.keys = {}
        get_width, get_height = manger.screen.get_size()
        self.width, self.height = get_width/2, get_height/2
        self.hp = 100
        self.max_hp = 100
        self.speed = 2.6
        self.jump_speed = -6
        self.mass = True
        self.on_ground = True
        self.tick = 1000
        self.last_update = 0
        
        
    def player_event(self, event : pygame.event.Event):
        
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
            if event.key == pygame.K_UP and self.on_ground:
                self.jump()
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False
    
    def update(self, mod):  
        
        if mod == 'play':
            if self.keys.get(pygame.K_RIGHT):
                self.direction.x = self.speed
                self.motion = 'forward'
            if self.keys.get(pygame.K_LEFT):
                self.direction.x = -self.speed
                self.motion = 'backward'
            if self.keys.get(pygame.K_0):
                if pygame.time.get_ticks() - self.last_update > self.tick:
                    self.last_update = pygame.time.get_ticks()
                    self.motion = 'jump'
                    sx, sy = self.position
                    AllyShot("shot", (sx, sy-50), self.look_mouse() * 5)
        elif mod == 'story':
            pass

        self.image = self.animation_controller.update()
        
        super().update(mod)
        
        for enemy in enemy_group.sprites():
            if self.recognition_range.colliderect(enemy.recognition_range):
                enemy.attack(self)
                
        collision = pygame.sprite.spritecollide(self, enemy_shot_group, True)
        
        for collide in collision:
            self.hp -= collide.power
            collide.remove()
            
            
        if self.rect_position[0] > self.width * 0.85:
            camera.x += 1

        if self.rect_position[0] < self.width * 0.25:
            camera.x -= 1

        #animation 

    def look_mouse(self):
        cx, cy = manger.camera.vector
        mx, my = pygame.mouse.get_pos()
        mouse_look = self.look_angle((mx + cx, my + cy))
        return mouse_look

    def destroy(self):
        super().destroy()
        manger.game.game_over = True
        manger.game.is_running = False
        
    def jump(self):
        self.add_force(0, self.jump_speed)
        self.on_ground = False
    
    @staticmethod
    def instantiate(json: Dict):
        return Player(json['name'], json['position'])