import pygame
from pygame.sprite import Group
from .sprites.background import BlcakRectangle
from typing import List
from time import sleep
from .sprites.background import BackGround
from .sprites.ui_sprite import Button
from . import color

UI = 'ui'
BACKGROUND = 'background'

class Scene:
    
    def __init__(self, screen):
        self.screen : pygame.Surface= screen
        
        self.background_layer = Group(
            BackGround(self.screen.get_size(), './src/sprites/image/main_image.png')
        )
        
        
        self.ui_layer = Group(
            Button((50, 50), (500, 400), "Wave", color.WHITE, "src\sprites\image\default.jpg", "src\sprites\image\click.jpg")
        )
        
        width, self.rect_height = self.screen.get_size()
        self.rect_width = width // 8
        self.nomarl_width = self.rect_width
        self.rects = Group()
        for i in range(8):
            rect = BlcakRectangle((self.nomarl_width, self.rect_height), (self.rect_width, 0))
            rect.image.set_alpha(0)
            self.rect_width += self.nomarl_width
            self.rects.add(rect)
        
    def update(self, layers=[]):
        
        if BACKGROUND not in layers: 
            self.background_layer.update()
            self.background_layer.draw(self.screen)
        
        
        if UI not in layers:
            self.ui_layer.update()
            self.ui_layer.draw(self.screen)
        
        
        
    def darkening_scene(self):
        for i in range(0, 39):  
            Sprites : List[BlcakRectangle] = self.rects.sprites()
            for j in Sprites:
                if Sprites.index(j) > i:
                    break
                alpha = j.image.get_alpha()
                alpha += 8
                j.image.set_alpha(alpha)
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(0.01)

    def brightening_scene(self):
        self.rect_width = self.nomarl_width
        
        for i in range(0, 39):
            Sprites : List[BlcakRectangle] = self.rects.sprites()
            for j in Sprites:
                if Sprites.index(j) > i:
                    break
                alpha = j.image.get_alpha()
                j.image.set_alpha(alpha - 8)
            self.update()
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(0.01)
        self.rects.empty()
    
    def scene_change(self):
        self.darkening_scene()
        self.brightening_scene()