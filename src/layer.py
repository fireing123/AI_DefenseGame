import pygame


class ObjectLayer(pygame.sprite.Group):
    
    def __init__(self, *sprites):
       super().__init__()
       
    @staticmethod
    def load(json):
        return ObjectLayer()


        

from .sprites.ui import Button, Text
class UILayer(pygame.sprite.Group):
    
    def __init__(self, *sprites):
        super().__init__()

    @staticmethod
    def load(json):
        ui = []
        try:
            ui += [Button.load(i) for i in json['buttons']]
        except KeyError: 
            print("not include button?!")
        try:
            ui += [Text.load(i) for i in json['texts']]
        except KeyError:
            print("not include text?!")
        
        return UILayer(ui)
