import json
from pygame import Surface
from pygame import time
from typing import Dict, List
from object import GameObject


class Animation:
    
    def __init__(self, surface_list : List[Surface], tick=500):
        self.index = 0
        self.tick = tick
        self.image_list : List[Surface] = surface_list
        self.len = len(self.image_list)
        self.last_update : int = 0
    
    def update(self) -> Surface:
        if time.get_ticks() - self.last_update > self.tick:
            if self.len <= self.index:
                return self.image_list[self.index]
            self.last_update = time.get_ticks()
            image = self.image_list[self.index]
            self.index += 1
        return image


class AnimationText:
    def __init__(self, string, scales, ticks):
        self.string = string
        self.scales = scales
        self.ticks = ticks
        self.index = 0
        
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if len(self.string) <= self.index:
            raise StopIteration
        self.index += 1
        return self.string[self.index -1], self.scales[self.index -1], self.ticks[self.index -1]
    
    @staticmethod
    def load(path):
        file = open(path, 'r')
        json_file = json.load(file.read())
        return __class__(
            json_file['string'],
            json_file['scale'],
            json_file['tick']
        )

class AnimationController:
    
    def __init__(self, idle_animation):
        self.game_object : GameObject
        self.str : str
        self.animation : Dict[str, Animation] = idle_animation
    
    def add(self, str, value) -> None:
        self.animation[str] = value
    
    def update(self) -> None:
        animation = self.animation[self.str]
        self.game_object.image = animation.update()
    
    def animation_translate(self, next_animation : str) -> None:
        self.str = next_animation
        for _, value in self.animation.items():
            value.index = 0
    
