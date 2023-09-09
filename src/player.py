import os
import pygame
import threading
import time
from typing import Dict
#not import my module
import manger
from object import LivingObject
from camera import camera
#import module first
from weapon import enemy_shot_group, BombShot, AllyShot
from enemy import enemy_group
from manger import enemy_death

class Player(LivingObject):

    def __init__(self, name: str, position):
        super().__init__(name, position, os.getcwd()+'/src/image/ai/config.xml')
        manger.player = self
        self.exp_bar = manger.ExpBar(name+"expBar", self)
        self.keys = {}
        get_width, get_height = manger.screen.get_size()
        self.width, self.height = get_width/2, get_height/2
        self.hp = 100
        self.max_hp = 100
        self.speed = 2.6
        self.jump_speed = -4
        self.mass = True
        self.on_ground = True
        self.tick = 200
        self.last_update = 0
        self.__exp = 0
        self.max_exp = 1000
        self.__lv = 0
        self.is_on = False
        self.is_pressing = False
        self.skill_q = 200
        self.skill_q_ev = True
        self.skill_w = 200
        self.skill_w_ev = False
        self.skill_e = 200
        self.skill_e_ev = False
        self.last_skill_q = 0
        self.last_skill_w = 0
        self.last_skill_e = 0

        enemy_death.add_lisner(self.add_exp)

    def add_exp(self, exp):
        self.exp += exp

    @property
    def exp(self):
        return self.__exp
    
    @exp.setter
    def exp(self, value):
        self.__exp = value
        if self.__exp > self.max_exp:
            self.exp -= self.max_exp
            self.lv += 1
    
    @property
    def lv(self):
        return self.lv
    
    @lv.setter
    def lv(self, value):
        lv_up = False
        if self.__lv < value:
            lv_up = True
        self.__lv = value
        if lv_up:
            self.level_up(value)
        
    def level_up(self, lv):
        pass
       
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
            if self.keys.get(pygame.K_q):
                if self.skill_q_ev: 
                    if pygame.time.get_ticks() - self.last_skill_q > self.skill_q:
                        self.last_skill_q = pygame.time.get_ticks()
                        BombShot("shot", self.position, self.look_mouse()*10)
            if self.keys.get(pygame.K_w):
                if self.skill_w_ev:
                    if pygame.time.get_ticks() - self.last_skill_w > self.skill_w:
                        self.last_skill_w = pygame.time.get_ticks()
                        self.speed = 5
                        def sped():
                            time.sleep(5)
                            self.speed = 2.6
                        threading.Thread(target=sped).start()
            if self.keys.get(pygame.K_e):
                if self.skill_e_ev:
                    if pygame.time.get_ticks() - self.last_skill_e > self.skill_e:
                        self.last_skill_e = pygame.time.get_ticks()
                        self.tick = 100
                        def ticd():
                            time.sleep(3)
                            self.tick = 200
                        threading.Thread(target=ticd).start()
            mouse_press = pygame.mouse.get_pressed()[0]

            if mouse_press:
                self.is_on = not self.is_pressing
            self.is_pressing = mouse_press
            
            if self.is_on:
                if pygame.time.get_ticks() - self.last_update > self.tick:
                    self.last_update = pygame.time.get_ticks()
                    manger.sound_manger['shot'].play()
                    AllyShot("shot", self.position, self.look_mouse()*10)
            if self.rect_position[0] > self.width * 0.9:
                camera.x += 1
            if self.rect_position[0] < self.width * 0.25:
                camera.x -= 1

            if self.rect_position[1] > self.height * 0.9:
                camera.y += 1

            if self.rect_position[1] < self.height * 0.25:
                camera.y -= 1
                
            if self.status == 'moving':
                if not self.step:
                    manger.sound_manger['step_forest'].play(-1)
                self.step = True
            elif self.status == 'idle':
                manger.sound_manger.stop('step_forest')
                self.step = False
        elif mod == 'story':
            pass
        
        
        
        super().update(mod)
        
        for enemy in enemy_group.sprites():
            if self.recognition_range.colliderect(enemy.recognition_range):
                enemy.attack(self)
                
        collision = pygame.sprite.spritecollide(self, enemy_shot_group, True)
        
        for collide in collision:
            self.hp -= collide.power
            collide.delete()

    def look_mouse(self):
        cx, cy = manger.camera.vector
        mx, my = pygame.mouse.get_pos()
        mouse_look, _ = self.look_angle((mx + cx, my + cy))
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