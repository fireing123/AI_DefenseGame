from pygame.sprite import Sprite
from pygame import Surface

class GameObject(Sprite):
    """
    기본 오브젝트
    """
    def __init__(self, layer = 3):
        self.layer_int = layer
        
    def render(self, surface : Surface):
        pass
    
