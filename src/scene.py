import pygame
from time import sleep
from typing import List
from pygame.sprite import Group
import manger
from background import BlcakRectangle

class Scene:
    
    def __init__(self):
        width, self.rect_height = manger.screen.get_size()
        self.rect_width = width // 8
        self.nomarl_width = self.rect_width
        self.rects = Group()
        for i in range(8):
            rect = BlcakRectangle((self.nomarl_width, self.rect_height), (self.rect_width, 0))
            rect.image.set_alpha(0)
            self.rect_width += self.nomarl_width
            self.rects.add(rect)
    
    def darkening_scene(self):

        for i in range(0, 39):  
            Sprites : List[BlcakRectangle] = self.rects.sprites()
            
            for j in Sprites:
                if Sprites.index(j) > i:
                    break
                alpha = j.image.get_alpha()
                alpha += 8
                j.image.set_alpha(alpha)
            manger.layers.render()
            self.rects.draw(manger.screen)
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
            
            manger.layers.update()
            manger.layers.render()
            self.rects.draw(manger.screen)
            pygame.display.flip()
            sleep(0.01)