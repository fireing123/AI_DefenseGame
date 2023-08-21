from pygame.sprite import Sprite
from pygame import Surface
from typing import Dict

class GameObject(Sprite):
    """
    기본 오브젝트
    """
    def __init__(self, name : str, layer = 3):
        self.layer_int = layer
        self.image : Surface
        self.name = name
                
    def render(self, surface : Surface):
        pass

    @staticmethod
    def instantiate(json : Dict):
        pass
