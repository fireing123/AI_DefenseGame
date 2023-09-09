import os
import pygame
from typing import Dict
from pygame.sprite import Group
from object import LivingObject
from weapon import shot_group, EnemyShot

enemy_group = Group()

class LivingEnemy:
    def __init__(self):
        self.int = 0
        
    def add(self, value):
        self.int += value
        
    def sub(self, value):
        self.int -= value
        
    def is_emty(self):
        return self.int == 0
        
living_enemy = LivingEnemy()

moving = [
    1,
    -1,
    1,
    0
]

class Enemy(LivingObject):
    """
    """
    def __init__(self, name, position, xml_path):
        super().__init__(name, position, xml_path)
        self.index = 1
        self.moving = 500
        self.last_moving = 0
        global living_enemy
        living_enemy.add(1)
        enemy_group.add(self)
    
    def update_index(self):
        if self.index >= len(moving):
            self.index = 1
        self.index += 1
    
    def update(self, mod):
        super().update(mod)
        if pygame.time.get_ticks() - self.last_moving > self.moving:
            self.last_moving = pygame.time.get_ticks()
            self.update_index()
        self.direction.x = moving[self.index - 1]
        collision = pygame.sprite.spritecollide(self, shot_group, True)
        for collide in collision:
            self.hp -= collide.power
            collide.delete()

    def attack(self, player):
        pass
    
    def delete(self):
        global living_enemy
        living_enemy.sub(1)
        super().delete()

class BigGuy(Enemy):
    def __init__(self, name, position):
        super().__init__(name, position, os.getcwd()+'/src/image/BigGuy/config.xml')
        self.hp = 500
        self.max_hp = 500
        self.tick = 800
        self.last_update = 0

    def attack(self, player):
        vec, angle = self.look_angle(player.position)
        if angle > 0:
            self.move = 'backward'
        else:
            self.move = 'forward'
        if pygame.time.get_ticks() - self.last_update > self.tick:
            self.last_update = pygame.time.get_ticks()
            EnemyShot("ew", self.position, vec * 5).power = 10
            
    @staticmethod
    def instantiate(json: Dict):
        return BigGuy(
            json['name'],
            json['position']
        )

class SuperSoldier(Enemy):
    def __init__(self, name, position):
        super().__init__(name, position, os.getcwd()+'/src/image/superSoldier/config.xml')
        self.hp = 200
        self.max_hp = 200
        self.tick = 400
        self.last_update = 0

    def attack(self, player):
        vec, angle = self.look_angle(player.position)
        if angle > 0:
            self.move = 'backward'
        else:
            self.move = 'forward'
        if pygame.time.get_ticks() - self.last_update > self.tick:
            self.last_update = pygame.time.get_ticks()
            EnemyShot("ew", self.position, vec * 5).power = 25

    @staticmethod
    def instantiate(json: Dict):
        return SuperSoldier(
            json['name'],
            json['position']
        )

class Soldier(Enemy):
    
    def __init__(self, name, position):
        super().__init__(name, position, os.getcwd()+'/src/image/soldier/config.xml')
        self.hp = 100
        self.max_hp = 100
        self.tick = 200
        self.last_update = 0

    
    def attack(self, player):
        vec, angle = self.look_angle(player.position)
        if angle > 0:
            self.move = 'backward'
        else:
            self.move = 'forward'
        if pygame.time.get_ticks() - self.last_update > self.tick:
            self.last_update = pygame.time.get_ticks()
            EnemyShot("ew", self.position, vec * 5)
    
    @staticmethod
    def instantiate(json: Dict):
        return Soldier(
            json['name'],
            json['position']
        )