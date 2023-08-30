import pygame
from layer import Layers

screen : pygame.Surface
layers : Layers

from background import * #object
from ground import * # object
#import module second
from ui import * # event, object, sheet(color), animation(object)
from player import * # object, animation(object), sheet(color), ground(object)
from enemy import *    
from core import *

def load_game_object(json):
    for name in json.keys():
        class_object : GameObject = globals()[name]
        for ject in json[name]:
            class_object.instantiate(ject)
