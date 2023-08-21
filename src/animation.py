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
    
    def __init__(self, list, tick=500):
        self.index = 0
        self.wait_tick = tick
        self.image_list : List[Surface] = list
        self.len = len(self.image_list)
        self.last_update = 0
    
    def update(self):
        if time.get_ticks() - self.last_update > self.wait_tick:
            if self.len <= self.index:
                return self.image_list[self.index]
            self.last_update = time.get_ticks()
            image = self.image_list[self.index]
            self.index += 1
        return image
