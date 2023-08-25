from pygame.sprite import Sprite
from pygame import Surface, Rect
from typing import Dict

class Component:
    
    def awake(self):
        pass
    
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

class LivingObject(GameObject):
    
    def __init__(self, name):
        super().__init__(name, 3)
        self.is_jumping = True