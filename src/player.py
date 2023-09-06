import pygame
import math
from typing import Dict, List
#not import my module
import manger
from object import LivingObject
from camera import camera
#import module first
from weapon import enemy_shot_group, BombShot
from enemy import enemy_group
from manger import enemy_death

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
        self.exp = 0
        self.lv = 0
        self.is_on = False
        self.is_pressing = False
        enemy_death.add_lisner(self.add_exp)
        
    def add_exp(self, value):
        self.exp += value
        self.lv = self.exp ** 0.4 * 49/50+1
        
    def player_event(self, event : pygame.event.Event):
        
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
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
            if self.keys.get(pygame.K_UP) and self.on_ground:
                self.jump()
                self.motion = 'jump'
            mouse_press = pygame.mouse.get_pressed()[0]

            if mouse_press:
                self.is_on = not self.is_pressing
            self.is_pressing = mouse_press
            
            if self.is_on:
                if pygame.time.get_ticks() - self.last_update > self.tick:
                    self.last_update = pygame.time.get_ticks()
                    sx, sy = self.position
                    BombShot("shot", (sx, sy-50), self.look_mouse()*10)
            if self.rect_position[0] > self.width * 0.9:
                camera.x += 1
            if self.rect_position[0] < self.width * 0.25:
                camera.x -= 1

            if self.rect_position[1] > self.height * 0.9:
                camera.y += 1

            if self.rect_position[1] < self.height * 0.25:
                camera.y -= 1
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
            
            
        

    def look_mouse(self):
        cx, cy = manger.camera.vector
        mx, my = pygame.mouse.get_pos()
        mouse_look = self.look_angle((mx + cx, my + cy))
        return mouse_look

    def destroy(self):
        manger.game.game_over = True
        manger.game.is_running = False
        
    def jump(self):
        self.add_force(0, self.jump_speed)
        self.on_ground = False
    
    @staticmethod
    def instantiate(json: Dict):
        return Player(json['name'], json['position'])