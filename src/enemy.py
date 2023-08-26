
from pygame import Surface
from object import GameObject


class Enemy(GameObject):
    """
    """
    def __init__(self, name):
        super().__init__(name)

class Soldier(Enemy):
    """
    적군인 오브젝트 전진, 발사기능이 있음
    """
    
    def __init__(self, name):
        super().__init__(name)
        self.health = 100
    
    def update(self):
        pass
    
    def render(self, surface: Surface, camera: tuple):
        pass
    
    