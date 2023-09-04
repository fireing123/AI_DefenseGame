import pygame
from layer import Layers
from event import Event
from scene import Scene

screen : pygame.Surface
scene : Scene
layers = Layers()

enemy_death = Event()

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
