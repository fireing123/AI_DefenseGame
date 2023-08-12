import pygame
from .sprites.background import BackGround

class BackgroundLayer(pygame.sprite.Group):
    
    def __init__(self, *sprites, screen):
        super().__init__()
        self.screen = screen
        
    @staticmethod
    def load(json, screen):
        return BackgroundLayer(
            BackGround(screen.get_size(), json)    
        )

class ObjectLayer(pygame.sprite.Group):
    
    def __init__(self, *sprites, screen):
        super().__init__()
       
    @staticmethod
    def load(json, screen):
        pass



class UILayer(pygame.sprite.Group):
    
    def __init__(self, *sprites):
        super().__init__()
       
    @staticmethod
    def load(json):
        pass