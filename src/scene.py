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
        self.rects = Group()
        
    def darkening_scene(self):
        for i in range(0, 16):
            if i < 8:
                rect = BlackBoxSprite((self.nomarl_width, self.rect_height), (self.rect_width, 0))
                rect.image.set_alpha(0)
                self.rect_width += self.nomarl_width
                self.rects.add(rect)
            Sprites : List[BlackBoxSprite] = self.rects.sprites()
            for j in Sprites:
                alpha = j.image.get_alpha()
                alpha += 16
                if alpha > 128 : alpha = 128
                print(alpha, end=" | ")
                j.image.set_alpha(alpha)
            print("\n----------")
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(0.2)

    def brightening_scene(self, func):
        self.rect_width = self.nomarl_width
        
        for i in range(0, 12):
            Sprites : List[BlackBoxSprite] = self.rects.sprites()
            self.test_log("he")
            for j in Sprites:
                self.test_log("he")
                if Sprites.index(j) > i:
                    break
                self.rects.draw(self.screen)
                pygame.display.flip()
                alpha = j.image.get_alpha()
                print(alpha)
                j.image.set_alpha(alpha - 32)
                if alpha - 32 <= 0:
                    self.rects.remove(j)
            func()
            self.rects.draw(self.screen)
            pygame.display.flip()
            sleep(1)
    
    def test_log(self, print_log):
        print(print_log)
        sleep(2)
    
    def scene_change(self, func):
        self.darkening_scene()
        self.brightening_scene(func)
    
class BlackBoxSprite(pygame.sprite.Sprite):
    def __init__(self, size, coordinate):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color.BLACK)
        self.rect = self.image.get_rect()
        self.rect.topright = coordinate
