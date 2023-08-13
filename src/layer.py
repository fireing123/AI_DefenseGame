import pygame



def object_load(json):
    return pygame.sprite.Group()


        

from .sprites.ui import Button, Text

def ui_load(json):
    ui = []
    try:
        ui += [Button.load(i) for i in json['buttons']]
    except KeyError: 
        print("not include button?!")
    try:
        ui += [Text.load(i) for i in json['texts']]
    except KeyError:
        print("not include text?!")
    
    return pygame.sprite.Group(*ui)
