from pygame import Surface
from pygame import time
from typing import Dict, List
from object import GameObject


class AnimationController:
    
    def __init__(self, idle_animation):
        self.game_object : GameObject
        self.str : str
        self.animation : Dict[str, Animation] = idle_animation
    
    def add(self, str, value):
        self.animation[str] = value
    
    def update(self):
        animation = self.animation[self.str]
        self.game_object.image = animation.update()
    
    def animation_translate(self, next_animation : str):
        self.str = next_animation
        for _, value in self.animation.items():
            value.index = 0
    
class Animation:
    
    def __init__(self, tick):
        self.index = 0
        self.wait_tick = tick
        self.image_list : List[Surface]
        self.len = len(self.image_list)
    
    def update(self):
        if time.get_ticks() - last_update > self.wait_tick:
            last_update = time.get_ticks()
            image = self.image_list[self.index]
            self.index += 1
        return image
