import os
import pygame
import threading
import time
from typing import Dict
import manger
from object import LivingObject
from camera import camera
from animation import Animation
from sheet import SpriteSheet
from weapon import enemy_shot_group, BombShot, AllyShot
from enemy import enemy_group

class Player(LivingObject):

    def __init__(self, name: str, position):
        super().__init__(name, position, './image/ai/config.xml')
        manger.player = self
        red_ani = SpriteSheet('./image/PowerfullAi/config.xml')
        self.animation_controller.add(
            "red",
            Animation(red_ani.items())
        )
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
        self.is_on = False
        self.is_pressing = False
        self.skill_q = 2000
        self.skill_q_ev = True
        self.skill_w = 6000
        self.skill_w_ev = False
        self.skill_e = 6000
        self.skill_e_ev = False
        self.last_skill_q = 0
        self.last_skill_w = 0
        self.last_skill_e = 0
       
    def player_event(self, event : pygame.event.Event):
        
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False
    
    def update(self, mod):  
        
        if mod == 'play':
            if self.keys.get(pygame.K_d):
                self.direction.x = self.speed
                self.motion = 'forward'
            if self.keys.get(pygame.K_a):
                self.direction.x = -self.speed
                self.motion = 'backward'
            if self.keys.get(pygame.K_w) and self.on_ground:
                self.jump()
                self.motion = 'jump'
            if self.keys.get(pygame.K_q):
                if self.skill_q_ev: 
                    if pygame.time.get_ticks() - self.last_skill_q > self.skill_q:
                        self.last_skill_q = pygame.time.get_ticks()
                        BombShot("shot", self.position, self.look_mouse()*10)
                        def sped():
                            self.skill_q_ev = False
                            time.sleep(2)
                            self.skill_q_ev = True
                        threading.Thread(target=sped).start()
            if self.keys.get(pygame.K_e):
                if self.skill_w_ev:
                    if pygame.time.get_ticks() - self.last_skill_w > self.skill_w:
                        self.last_skill_w = pygame.time.get_ticks()
                        self.speed = 5
                        def sped():
                            self.skill_w_ev = False
                            time.sleep(3)
                            self.speed = 2.6
                            time.sleep(3)
                            self.skill_w_ev = True
                        threading.Thread(target=sped).start()
            if self.keys.get(pygame.K_r):
                if self.skill_e_ev:
                    if pygame.time.get_ticks() - self.last_skill_e > self.skill_e:
                        self.last_skill_e = pygame.time.get_ticks()
                        self.tick = 100
                        self.animation_controller.animation_translate('red')
                        def ticd():
                            self.skill_e_ev = False
                            time.sleep(3)
                            self.animation_controller.animation_translate('idle')
                            self.tick = 200
                            time.sleep(3)
                            self.skill_e_ev = True
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
                camera.x += 3
            if self.rect_position[0] < self.width * 0.25:
                camera.x -= 3

            if self.rect_position[1] > self.height * 0.9:
                camera.y += 3

            if self.rect_position[1] < self.height * 0.25:
                camera.y -= 3
                
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