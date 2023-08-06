import pygame
from pygame.sprite import Group
from typing import Any, List
from time import sleep
import color
class SceneLoad:
    
    def __init__(self, screen):
        self.screen : pygame.Surface= screen
        width, self.rect_height = self.screen.get_size()
        self.rect_width = width // 8
        self.nomarl_width = self.rect_width
        self.rects : List[BlackBoxSprite] = []
        
    def darkening_scene(self):
        for i in range(8):
            rect = BlackBoxSprite(self.rect_width/2, self.rect_height/2)
            self.rect_width += self.nomarl_width
            self.rects[i] = rect
            for j in self.rects:
                alpha = j.image.get_alpha()
                j.image.set_alpha(alpha + 32)
                self.screen.blit(j)
                sleep(1)

    def brightening_scene(self):
        self.rect_width = self.nomarl_width
        for i in range(8):
            self.rect_width += self.nomarl_width
            for j in self.rects:
                alpha = j.image.get_alpha()
                j.image.set_alpha(alpha - 32)
                self.screen.blit(j)
                sleep(1)

    def SceneChange(self, init):
        def decorator(func):
            def wapper(*args, **kwargs):
                self.darkening_scene()
                init()
                self.brightening_scene()
                return func(*args, **kwargs)
            return wapper
        return decorator
    
class BlackBoxSprite(pygame.sprite.Sprite):
    def __init__(self, wd, hg):
        super().__init__()
        self.image = pygame.Surface((wd, hg), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0,0,0,0), pygame.Rect(0, 0, wd, hg))
