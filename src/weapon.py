import pygame
import math
from object import GameObject
from object import MoveObject

class Weapon(GameObject):
    def __init__(self, name: str):
        super().__init__(name)
    
    
    
class Shot(MoveObject):
    def __init__(self, name, position, direction):
        super().__init__(name)
        self.image = pygame.image.load('src/image/shot.png')
        self.rect = self.image.get_rect()
        self.position = position
        self.direction = pygame.Vector2(*direction)
 
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