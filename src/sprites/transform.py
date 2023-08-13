from pygame.math import Vector2
import pygame


class Transform:
    
    def __init__(self, 
                position : Vector2,
                rotation : Vector2,
                scale    : Vector2,
                children : pygame.sprite.Group):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.children = children
        
    def __setattr__(self):
        pass