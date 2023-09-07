import json
from pygame import Surface
from pygame import time
from typing import Dict, List

class Animation:
    
    def __init__(self, surface_list : List[Surface], loop=True, tick=500):
        self.index = 0
        self.tick = tick
        self.image_list : List[Surface] = surface_list
        self.len = len(self.image_list)
        self.last_update : int = 0
        self.is_loop = loop
    
    def update(self):
        if time.get_ticks() - self.last_update > self.tick:
            if self.is_loop and self.index >= self.len:
                self.index = 0
            elif self.index >= self.len:
                return self.image_list[-1], True
            self.last_update = time.get_ticks()
            self.index += 1
        return self.image_list[self.index-1], False


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
        file = open(path, 'r', encoding='UTF-8')
        json_file = json.loads(file.read())
        
        file.close()
        return __class__(
            json_file['string'],
            json_file['scale'],
            json_file['tick']
        )

class AnimationController:
    
    def __init__(self, idle_animation, game_object):
        self.game_object = game_object
        self.str : str = 'idle'
        self.animation : Dict[Surface] = {}
        self.animation[self.str] = idle_animation
    

    
    def add(self, str, value):
        self.animation[str] = value
    
    def update(self):
        animation = self.animation.get(self.str)
        if not animation:
            #print(f'None Animation {self.str}')
            animation = self.animation.get('idle')
        image, _ = animation.update()
        return image
    
    def animation_translate(self, next_animation : str) -> None:
        if self.str != next_animation:
            self.str = next_animation
            for _, value in self.animation.items():
                value.index = 0
    
