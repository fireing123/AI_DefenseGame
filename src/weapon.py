import pygame
import math
from object import MoveObject
    
shot_group = pygame.sprite.Group()
    
class Shot(MoveObject):
    def __init__(self, name, position, direction):
        super().__init__(name)
        self.image = pygame.image.load('src/image/shot.png')
        self.power = 10
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = pygame.Vector2(*direction)
        shot_group.add(self)
 
    def update(self):
        super().update()
        
        angle_rad = math.atan2(*self.direction)
        self.angle = math.degrees(angle_rad)
        if self.collision:
            self.remove()
        
    def render(self, surface: pygame.Surface, camera: tuple):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        super().render(surface, camera)