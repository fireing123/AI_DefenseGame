import pygame
import math
from object import MoveObject, GameObject
    
shot_group = pygame.sprite.Group()
    
enemy_shot_group = pygame.sprite.Group()
    
class Gun(GameObject): pass

    
class Shot(MoveObject):
    def __init__(self, name, position, direction):
        super().__init__(name)
        self.image = pygame.image.load('src/image/shot.png')
        self.power = 10
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = pygame.Vector2(*direction)
        self.gravity = 0.01
        self.air_friction = 1
 
    def destroy(self):
        pass
 
    def update(self):
        super().update()
        
        angle_rad = math.atan2(*self.direction)
        self.angle = math.degrees(angle_rad)
        if self.collision:
            self.destroy()
            self.remove()
        
    def render(self, surface: pygame.Surface, camera: tuple):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(rotated_image, self.rect_position)
        
class AllyShot(Shot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        shot_group.add(self)
        
class EnemyShot(Shot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        
    def render(self, surface, camera: tuple):
        super().render(surface, camera)
        enemy_shot_group.add(self)