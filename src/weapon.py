import pygame
import math
from object import GameObject
from object import MoveObject

class Weapon(GameObject):
    def __init__(self, name: str):
        super().__init__(name)
    
    
    
class Shot(MoveObject):
    def __init__(self, name, direction):
        super().__init__(name)
        self.direction = pygame.Vector2(*direction)
 
    def update(self):
        super().update()
        
        angle_rad = math.atan2(*self.direction)
        self.angle = math.degrees(angle_rad)
        if self.collision:
            pass
        
    def render(self, surface: pygame.Surface, camera: tuple):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(self.image, self.rect_position)