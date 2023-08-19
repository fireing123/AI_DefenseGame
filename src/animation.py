from typing import Dict, List

class AnimationController:
    
    def __init__(self, idle_animation):
        self.str : str
        self.animation : Dict[str, Animation] = idle_animation
    
    def update(self):
        pass
    
    def animation_translate(self, next_animation : str, time : float):
        pass
    
class Animation:
    
    def __init__(self):
        self.index = 0
        self.image_list : List
    
    def update(self):
        image = self.image_list[self.index]
        self.index += 1
        return image