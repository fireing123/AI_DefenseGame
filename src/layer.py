from typing import List
#not import my module
from object import GameObject
#import module first
from background import * #object
from ground import * # object
#import module second
from ui import * # event, object, sheet(color), animation(object)
from player import * # object, animation(object), sheet(color), ground(object)

class Layers:
    """
    전체 오브젝트를 포함하고
    오브젝트의 공통 함수를 실행합니다.
    """
    def __init__(self, *objects):
        self.layers : list[list[GameObject]] = [[],[],[],[],[]]
        self.absorb(objects)
       
    def add(self, game_object: GameObject):
        layer_int = game_object.layer_int
        layer = self.layers[layer_int]
        layer.append(game_object)
    
    def absorb(self, list : List):
        for obj in list:
            self.add(obj)
         
    def in_layer_turning(self, method, *args):
        for layer in self.layers:
            for game_object in layer:
                try:
                    func = getattr(game_object, method)
                    func(*args)
                except AttributeError:
                    print(f"Function '{method}' not found in class '{game_object}'.")

    def get_game_object_by_name(self, name) -> GameObject:
        for y in self.layers:
            for x in y:
                if x.name == name:
                    return x
        return None

def load_game_object(json : dict) -> list[GameObject]:
    obj = []
    for name in json.keys():
        class_object : GameObject = globals()[name]
        for ject in json[name]:
            obj.append(class_object.instantiate(ject))
    return obj