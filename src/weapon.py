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
        self.direction = direction
        self.gravity = 0.01
        self.air_friction = 1
        self.angle = 0
    
    def destroy(self):
        pass
 
    def update(self, mod):
        super().update(mod)
        
        angle_rad = math.atan2(*self.direction)
        self.angle = math.degrees(angle_rad)
        if self.collision:
            self.destroy()
            self.remove()
        
    def render(self, surface: pygame.Surface, camera: tuple):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        #self.rect = rotated_image.get_rect(center=self.rect.center)
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(rotated_image, self.rect_position)
        
class AllyShot(Shot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        shot_group.add(self)
        
    def remove(self):
        shot_group.remove(self)
        return super().remove()
 
class BombShot(AllyShot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        self.rect = pygame.Rect(0, 0, 10, 20)
        self.position = position
    
    def on_collision_enter(self, collision):
        for r in range(1, 13):
            rr = r*30
            vec = pygame.Vector2(5, 0).rotate_rad(rr)
            AllyShot(f'{rr}/[{self.name}]', self.position, vec)
 
class EnemyShot(Shot):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        enemy_shot_group.add(self)

    def remove(self):
        enemy_shot_group.remove(self)
        return super().remove()