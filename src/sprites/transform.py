from pygame.math import Vector2
import pygame
from math import cos, sin, radians


class Transform:
    
    def __init__(self, 
                position : Vector2,
                rotation : Vector2,
                scale    : Vector2,
                parent   : pygame.sprite.Sprite | None,
                children : list[pygame.sprite.Sprite]):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.local_position : Vector2= position
        self.local_rotation : Vector2= rotation
        self.local_scale : Vector2= scale
        self.parent = parent
        self.children = children
        print("not include transform")
     
    def trans_handler(self):
        for child in self.children:
            transform : Transform= child.transform
            transform.local_position = self.local_position + transform.position
            transform.local_scale = self.local_scale + transform.scale
            self.local_position.distance_to(transform.local_position)
            x , y=self.local_position.x, self.local_position.y
            new_x = x * cos(radians(self.local_rotation)) - y * sin(radians(self.local_rotation))
            new_y = x * sin(radians(self.local_rotation)) + y * cos(radians(self.local_rotation))
            transform.local_position = Vector2(new_x, new_y)
            
    @property
    def position(self):
        return self.position
    
    @position.setter
    def position(self, new_value):
        self.position = new_value
        parent : Transform = self.parent.transform
        self.local_position = parent.local_position + self.position

        
    @property
    def local_position(self):
        return self.local_position
    
    @local_position.setter
    def local_position(self, new_value):
        self.local_position = new_value
        self.trans_handler()
        
    @property
    def rotation(self):
        return self.rotation
    
    @rotation.setter
    def rotation(self, new_value):
        self.rotation = new_value
        parent : Transform = self.parent.transform
        self.local_rotation = parent.local_rotation + self.rotation
        
    @property
    def local_rotation(self):
        return self.local_rotation
    
    @local_rotation.setter
    def local_rotation(self, new_value):
        self.local_rotation = new_value
        self.trans_handler()
            
    @property
    def scale(self):
        return self.scale
    
    @scale.setter
    def scale(self, new_value):   
        self.scale = new_value
        parent : Transform = self.parent.transform
        self.local_scale = parent.local_scale + self.scale

    @property
    def local_scale(self):
        return self.local_scale
    
    @local_scale.setter
    def local_scale(self, new_value):
        self.local_scale = new_value
        self.trans_handler()
