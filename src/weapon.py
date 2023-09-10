import os
import pygame
import manger
import math
from object import MoveObject
from camera import camera

shot_group = pygame.sprite.Group()
enemy_shot_group = pygame.sprite.Group()
    
class Shot(MoveObject):
    def __init__(self, name, position, direction):
        super().__init__(name)
        self.image = pygame.image.load('./image/shot.png')
        self.power = 10
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = direction
        self.gravity = 0
        self.air_friction = 1
        self.angle = 0
 
    def update(self, mod):
        if 0 > self.rect_position[0] or self.rect_position[0] > 1000:
            self.delete()
        if 0 > self.rect_position[1] or self.rect_position[1] > 800:
            self.delete()
        super().update(mod)
        
        angle_rad = math.atan2(*self.direction)
        self.angle = math.degrees(angle_rad)
        if self.collision:
            self.delete()
        
    def render(self, surface: pygame.Surface, camera: tuple):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        if not self.visible: return
        cx, cy = camera
        rx, ry = rotated_image.get_rect(center=self.rect.center).topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(rotated_image, self.rect_position)
        
class AllyShot(Shot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        camera.shiver()
        shot_group.add(self)

class SubShot(Shot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        shot_group.add(self)
        
class BombShot(AllyShot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        self.image = pygame.image.load('./image/bomb.png')
        self.rect = pygame.Rect(0, 0, 10, 20)
        self.position = position
    
    def on_collision_enter(self, collision):
        manger.sound_manger['boom'].play()
        for r in range(1, 13):
            rr = r*30
            vec = pygame.Vector2(5, 0).rotate_rad(rr)
            SubShot(f'{rr}/[{self.name}]', self.position, vec)
 
class EnemyShot(Shot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        enemy_shot_group.add(self)