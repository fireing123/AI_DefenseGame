import json
import pygame
from pygame.sprite import Group
from typing import List
from time import sleep
#not import my module
from camera import camera
#import module first
from background import BlcakRectangle
#import module third


class Scene:
    """
    개임의 맵을 담당함
    """
    def __init__(self, screen : pygame.Surface,
                layers):
        
        self.screen = screen
        self.layers = layers
        global seen
        global layer
        layer = layers
        seen = screen

        width, self.rect_height = screen.get_size()
        self.rect_width = width // 8
        self.nomarl_width = self.rect_width
        self.rects = Group()
        for i in range(8):
            rect = BlcakRectangle((self.nomarl_width, self.rect_height), (self.rect_width, 0))
            rect.image.set_alpha(0)
            self.rect_width += self.nomarl_width
            self.rects.add(rect)
        


    def update(self):
        self.layers.in_layer_turning('update')
        
    def render(self):
        self.layers.in_layer_turning('render', self.screen, camera.vector)
    
    
    @staticmethod
    def load(path, screen : pygame.Surface):
        file = open(path, 'r')
        json_file :dict = json.loads(file.read())
        file.close()
        objects = load_game_object(json_file)
        from layer import Layers
        layers = Layers(*objects)
        return Scene(screen, layers)
    
    
    def darkening_scene(self):

        for i in range(0, 39):  
            Sprites : List[BlcakRectangle] = self.rects.sprites()
            
            for j in Sprites:
                if Sprites.index(j) > i:
                    break
                alpha = j.image.get_alpha()
                alpha += 8
                j.image.set_alpha(alpha)
            self.render()
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(0.01)

    def brightening_scene(self):
        self.rect_width = self.nomarl_width
        for j in self.rects.sprites(): j.image.set_alpha(144)
        
        for i in range(0, 39):
            Sprites : List[BlcakRectangle] = self.rects.sprites()
            
            for j in Sprites:
                if Sprites.index(j) > i:
                    break
                
                alpha = j.image.get_alpha()
                j.image.set_alpha(alpha - 8)
            
            self.update()
            self.render()
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(0.01)        

from background import * #object
from ground import * # object
#import module second
from ui import * # event, object, sheet(color), animation(object)
from player import * # object, animation(object), sheet(color), ground(object)
from enemy import *

def load_game_object(json : dict) -> list[GameObject]:
    obj = []
    for name in json.keys():
        class_object : GameObject = globals()[name]
        for ject in json[name]:
            obj.append(class_object.instantiate(ject))
    return obj