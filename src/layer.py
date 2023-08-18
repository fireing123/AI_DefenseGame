import pygame
from .background import BackGround
# 탈피 막바지

def background_load(json, size):
    return BackGround(size, json)

def object_load(json):
    return pygame.sprite.Group()


class Layers:
    
    def __init__(self):
        self.layers : list[list] = [[],[],[],[]]
       
    def add(self,game_object):
        layer_int = game_object.layer_int
        layer = self.layers[layer_int]
        layer.append(game_object)
         
    def absorb(self, list):
        for obj in list:
            self.add(obj)
         
    def in_layer_turning(self, method, *args):
        for layer in self.layers:
            for game_object in layer:
                try:
                    func = getattr(game_object, method)
                    func(*args)
                except AttributeError:
                    print(f"Function '{func}' not found in class '{game_object}'.")

    



from .ui import Button, Text
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
    
    return ui
