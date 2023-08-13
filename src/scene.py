import pygame
import json
from pygame.sprite import Group
from .sprites.background import BlcakRectangle
from typing import List
from time import sleep
from .sprites.background import BackGround
from .sprites.ui import Button
from . import color
from .layer import UiLayer, object_load, ui_load
UI = 'ui'
OBJECTT = 'object'
BACKGROUND = 'background'



class Scene:
    screen : pygame.Surface
    background : BackGround
    object_layer : Group
    ui_layer : UiLayer
    
    def __init__(self, creen : pygame.Surface,
                ackground : BackGround, 
                bject_layer : Group, 
                i_layer : UiLayer):
        
        global screen
        global background
        global object_layer
        global ui_layer
        screen = creen
        background = ackground
        object_layer = bject_layer
        ui_layer = i_layer
        

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
        background.update()
        object_layer.update()
        ui_layer.update()
    
    def draw(self, layers = []):
        if BACKGROUND not in layers: 
            screen.blit(background.image, background.rect)
        if OBJECTT not in layers:
            object_layer.draw(screen)
        if UI not in layers:
            ui_layer.draw(screen)
    
    @staticmethod
    def load(json_path, screen : pygame.Surface):
        file = open(json_path, 'r')
        json_file = json.loads(file.read())
        file.close()
        return Scene(
                screen,
                BackGround(screen.get_size(), json_file['background']),
                object_load(json_file['object']),
                ui_load(json_file['ui'])
        )
    
    def scene_kill(self):
        object_layer.empty()
        ui_layer.empty()
    
    def darkening_scene(self):

        for i in range(0, 39):  
            Sprites : List[BlcakRectangle] = self.rects.sprites()
            
            for j in Sprites:
                if Sprites.index(j) > i:
                    break
                alpha = j.image.get_alpha()
                alpha += 8
                j.image.set_alpha(alpha)
            self.draw()
            self.rects.draw(screen)
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
            self.draw()
            self.rects.draw(screen)
            pygame.display.flip()
            sleep(0.01)
    
    def scene_change(self, path):
        self.darkening_scene()
        new_scene = Scene.load(path, screen)
        new_scene.brightening_scene()
        return new_scene