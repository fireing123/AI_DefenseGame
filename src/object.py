from pygame.sprite import Sprite
from pygame import Surface
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
    
    def render(self, surface : Surface):
        pass
    

class GameObject(Sprite, Component):
    """
    기본 오브젝트
    """
    def __init__(self, name : str, layer = 3):
        self.layer_int = layer
        self.image : Surface
        self.name = name
                

    @staticmethod
    def instantiate(json : Dict):
        pass

class LivingObject(GameObject):
    
    def __init__(self, name):
        super().__init__(name, 3)
        self.is_jumping = True