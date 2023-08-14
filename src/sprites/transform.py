from pygame.math import Vector2
import pygame
from math import cos, sin, radians

class Empty:
 
    local_position = Vector2(0, 0)
    local_rotation = 0
    local_scale = Vector2(1, 1)
        
    

class Transform:
    
    def __init__(self, 
                position : Vector2,
                rotation : float,
                scale    : Vector2,
                children : list[pygame.sprite.Sprite],
                parent=Empty):
        self.__position = position
        self.__rotation = rotation
        self.__scale = scale
        self.__parent = parent
        self.__local_position : Vector2 = position
        self.__local_rotation : float = rotation
        self.__local_scale : Vector2 = scale
        self.children = children
      
      
     
    def trans_handler(self):
        for child in self.children:
            transform : Transform = child.transform
            transform.__local_position = self.__local_position + transform.__position
            transform.__local_scale = self.__local_scale + transform.__scale
            self.__local_position.distance_to(transform.__local_position)
            x , y=self.__local_position.x, self.__local_position.y
            new_x = x * cos(radians(self.__local_rotation)) - y * sin(radians(self.__local_rotation))
            new_y = x * sin(radians(self.__local_rotation)) + y * cos(radians(self.__local_rotation))
            transform.__local_position = Vector2(new_x, new_y)
            
    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, new_value):
        self.__position = new_value
        parent : Transform | Empty = self.__parent
        self.local_position = parent.__local_position + self.__position

        
    @property
    def local_position(self):
        return tuple(self.__local_position)
    
    @local_position.setter
    def local_position(self, new_value):
        self.__local_position = new_value
        self.trans_handler()
        
    @property
    def rotation(self):
        return self.__rotation
    
    @rotation.setter
    def rotation(self, new_value):
        self.__rotation = new_value
        parent : Transform | Empty= self.parent
        self.local_rotation = parent.__local_rotation + self.__rotation
        
    @property
    def local_rotation(self):
        return self.__local_rotation
    
    @local_rotation.setter
    def local_rotation(self, new_value):
        self.__local_rotation = new_value
        self.trans_handler()
            
    @property
    def scale(self):
        return self.__scale
    
    @scale.setter
    def scale(self, new_value):   
        self.__scale = new_value
        parent : Transform | Empty= self.parent
        self.local_scale = parent.__local_scale + self.__scale

    @property
    def local_scale(self):
        return self.__local_scale
    
    @local_scale.setter
    def local_scale(self, new_value):
        self.__local_scale = new_value
        self.trans_handler()
