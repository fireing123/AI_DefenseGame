import pygame
from pygame.sprite import Sprite
from pygame import Surface, Rect
from typing import Dict

class Component:
    

    def start(self):
        pass
    
    def on_collision_enter(self):
        pass
    
    def on_mouse_pressed(self):
        pass
    
    def update(self):
        pass
    
    def render(self, surface : Surface, camera : tuple):
        pass
    
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __len__(self):
        return 2
    
    
    def __add__(self, other):
        return self.__class__(
            self.x + other.x,
            self.y + other.y
        )

    def __iadd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return self.__class__(
            self.x - other.x,
            self.y - other.y
        )
        
    def __isub__(self, other):
        return self.__sub__(other)
        
    def __mul__(self, other):
        return self.__class__(
            self.x * other.x,
            self.y * other.y
        )
    
    def __imul__(self, other):
        return self.__mul__(other)
        
    def __div__(self, other):
        return self.__class__(
            self.x / other.x,
            self.y / other.y
        )
        
    def __idiv__(self, other):
        return self.__div__(other)
    
class GameObject(Sprite, Component):
    """
    기본 오브젝트
    """
    
            
    def __init__(self, name : str, layer = 3):
        Sprite.__init__(self)
        self.rect_position = (0, 0)
        self.layer_int = layer
        self.image : Surface
        self.rect = Rect(0,0,0,0)
        self.name = name
        self.__position = Position(0, 0)

    def child_position(self):
        pass
        
    @property
    def position(self):
        return tuple(self.__position)

    @position.getter
    def position(self):
        return tuple(self.__position)
    
    @position.setter
    def position(self, value):
        self.__position = Position(*value)
        self.rect.center = self.position
        self.child_position()

    @staticmethod
    def instantiate(json : Dict):
        pass

from ground import group as ground_group

class MoveObject(GameObject):
    
    
    def __init__(self, name):
        super().__init__(name)
        self.gravity = 0.08
        self.direction = pygame.Vector2(0, 0)
        self.on_ground = False
        self.friction = 0.5
        self.air_friction = 0.6
        self.mass = True
        self.rect : pygame.Rect
        
    def update(self):
        
        self.direction.y += self.gravity
        
        self.collision = pygame.sprite.spritecollide(self, ground_group, False)
        if self.mass:
            self.direction.x *= self.friction
            if abs(self.direction.x) < 0.1:
                self.direction.x = 0
                
        if self.collision != None:
            for collide in self.collision:
                cox, coy = collide.rect.size
                cox, coy = cox/2, coy/2
                if self.rect.bottom < collide.rect.top + coy:
                    self.rect.bottom = collide.rect.top + 1
                    self.direction.y = self.cut_minus(self.direction.y)
                    self.on_ground = True
                else:
                    self.direction.y += self.gravity
                    if self.rect.top > collide.rect.bottom - coy:
                        #bottom
                        self.rect.top = collide.rect.bottom
                        self.direction.y = self.cut_plus(self.direction.y)
                    elif self.rect.left > collide.rect.right - 5:
                        #right
                        self.rect.left = collide.rect.right
                        self.direction.x = 0
                    elif self.rect.right < collide.rect.left + 5:
                        #left
                        self.rect.right = collide.rect.left
                        self.direction.x = 0
                self.on_collision_enter(collide)
        else:
            self.friction = self.air_friction
        self.position = self.rect.center
        self.position += self.direction
        
    def cut_plus(self, num):
        if num < 0:
            return 0
        else:
            return num
    
    def cut_minus(self, num):
        if num > 0:
            return 0
        else:
            return num
        
    def add_force(self, x=0, y=0):
        self.direction += pygame.Vector2((x, y))

class LivingObject(MoveObject):
    
    def __init__(self, name):
        super().__init__(name)
        self.__health = 100
       
    def destroy(self):
        pass
     
    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, value):
        self.__health = value
        if self.__health < 0:
            self.destroy()