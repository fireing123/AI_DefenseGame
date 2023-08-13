import pygame
import json
from pygame.sprite import Group
from .sprites.background import BlcakRectangle
from typing import List
from time import sleep
from .sprites.background import BackGround
from .sprites.ui import Button
from . import color
from .layer import ObjectLayer, UILayer
UI = 'ui'
OBJECTT = 'object'
BACKGROUND = 'background'

class Scene:
    
    def __init__(self, screen : pygame.Surface,
                background : BackGround, 
                object_layer : ObjectLayer, 
                ui_layer : UILayer):
        
        self.screen = screen
        
        self.background = background
        self.object_layer = object_layer
        self.ui_layer = ui_layer

        width, self.rect_height = self.screen.get_size()
        self.rect_width = width // 8
        self.nomarl_width = self.rect_width
        self.rects = Group()
        for i in range(8):
            rect = BlcakRectangle((self.nomarl_width, self.rect_height), (self.rect_width, 0))
            rect.image.set_alpha(0)
            self.rect_width += self.nomarl_width
            self.rects.add(rect)
        
    def update(self):
        self.background.update()
        self.object_layer.update()
        self.ui_layer.update()
    
    def draw(self, layers = []):
        if BACKGROUND not in layers: 
            self.screen.blit(self.background.image, self.background.rect)
        if OBJECTT not in layers:
            self.object_layer.draw(self.screen)
        if UI not in layers:
            self.ui_layer.draw(self.screen)
    
    @staticmethod
    def load(json_path, screen):
        file = open(json_path, 'r')
        json_file = json.loads(file.read())
        file.close()
        return Scene(
                screen,
                BackGround(screen.get_size(), json_file['background']),
                ObjectLayer.load(json_file['object']),
                UILayer.load(json_file['ui'])
        )


    
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