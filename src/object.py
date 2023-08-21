from pygame.sprite import Sprite
from pygame import Surface

class GameObject(Sprite):
    """
    기본 오브젝트
    """
    def __init__(self, name, layer = 3):
        self.layer_int = layer
        self.image : Surface
        self.name : str = name
                
    def render(self, surface : Surface):
        pass

    @staticmethod
    def instantiate(json):
        pass
