
from typing import Dict
from pygame import Surface
from object import LivingObject
from sheet import SpriteSheet
from animation import AnimationController

class Enemy(LivingObject):
    """
    """
    def __init__(self, name, position):
        super().__init__(name, position)

class Soldier(Enemy):
    """
    적군인 오브젝트 전진, 발사기능이 있음
    """
    
    def __init__(self, name, position):
        super().__init__(name, position)
        self.hp = 100
        self.max_hp = 100
        self.speed = 2
        idle_animation = SpriteSheet('src/image/soldier/config.xml')
        self.animation_controller = AnimationController(
            idle_animation.items(),
            self
        )
        self.image : Surface = idle_animation['default']
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def update(self):
        super().update()
    
    def render(self, surface: Surface, camera: tuple):
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(self.image, self.rect_position)
    
    @staticmethod
    def instantiate(json: Dict):
        return Soldier(
            json['name'],
            json['position']
        )