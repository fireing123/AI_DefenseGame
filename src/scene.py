import json
import pygame
from pygame.sprite import Group
from typing import List
from time import sleep
from background import BlcakRectangle
from layer import Layers, load_game_object

class Scene:
    """
    개임의 맵을 담당함
    """
    def __init__(self, screen : pygame.Surface,
                layers : Layers):
        
        self.screen = screen
        self.layers = layers

        width, self.rect_height = screen.get_size()
        self.rect_width = width // 8
        self.nomarl_width = self.rect_width
        self.rects = Group()
        for i in range(8):
            rect = BlcakRectangle((self.nomarl_width, self.rect_height), (self.rect_width, 0))
            rect.image.set_alpha(0)
            self.rect_width += self.nomarl_width
            self.rects.add(rect)
        

                
    def awake(self):
        self.layers.in_layer_turning('awake')
        
    def render(self):
        self.layers.in_layer_turning('render', self.screen)
    
    def update(self):
        self.layers.in_layer_turning('update')
    
    @staticmethod
    def load(json_path, screen : pygame.Surface):
        file = open(json_path, 'r')
        json_file :dict = json.loads(file.read())
        file.close()
        objects = load_game_object(json_file)
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
            self.render()
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(0.01)
    
    def scene_change(self, path):
        self.darkening_scene()
        new_scene = Scene.load(path, self.screen)
        del self
        new_scene.brightening_scene()
        return new_scene