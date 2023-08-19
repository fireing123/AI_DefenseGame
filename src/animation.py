from pygame import Surface
from typing import Dict, List
from object import GameObject

class AnimationController:
    
    def __init__(self, idle_animation):
        self.game_object : GameObject
        self.str : str
        self.animation : Dict[str, Animation] = idle_animation
    
    def update(self):
        animation = self.animation[self.str]
        self.game_object.image = animation.update()
    
    def animation_translate(self, next_animation : str):
        self.str = next_animation
        for _, value in self.animation.items():
            value.index = 0
    
class Animation:
    
    def __init__(self):
        self.index = 0
        self.image_list : List[Surface]
        self.len = len(self.image_list)
    
    def update(self):
        image = self.image_list[self.index]
        self.index += 1
        return image