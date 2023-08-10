import pygame
from pygame.sprite import Group
from sprites.background import BlcakRectangle
from typing import List
from time import sleep
from sprites.background import BackGround


class Scene:
    
    def __init__(self, screen):
        self.screen : pygame.Surface= screen
        
        self.background = BackGround(self.screen.get_size(), './src/sprites/image/main_image.png')
        
        self.ui_layer = Group()
        
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
        image = self.background.image
        rect = image.get_rect()
        self.screen.blit(image, rect)
        
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

    def brightening_scene(self, func):
        self.rect_width = self.nomarl_width
        
        for i in range(0, 39):
            Sprites : List[BlcakRectangle] = self.rects.sprites()
            for j in Sprites:
                if Sprites.index(j) > i:
                    break
                alpha = j.image.get_alpha()
                j.image.set_alpha(alpha - 8)
            func()
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(0.01)
        self.rects.empty()
    
    def scene_change(self, func):
        self.darkening_scene()
        self.brightening_scene(func)