import json
from typing import List
#import module first
import manger
from camera import camera

class Layers:
    """
    전체 오브젝트를 포함하고
    오브젝트의 공통 함수를 실행합니다.
    """
    def __init__(self, mod='play'):
        self.layers = [[],[],[],[],[]]
        self.mod = mod
       
    def remove(self, obj):
        layer = self.layers[obj.layer_int]
        try:
            layer.remove(obj)
        except ValueError:
            print("not in list")
       
    def add(self, game_object):
        layer_int = game_object.layer_int
        layer = self.layers[layer_int]
        layer.append(game_object)
    
    def absorb(self, list : List):
        for obj in list:
            self.add(obj)
         
    def in_layer_turning(self, method, *args):
        for layer in self.layers:
            for game_object in layer:
                #try:
                func = getattr(game_object, method)
                func(*args)
                #except AttributeError:
                #    print(f"Function '{method}' not found in class '{game_object}'.")

    def update(self):
        self.in_layer_turning('update', self.mod)
        
    def render(self):
        self.in_layer_turning('render', manger.screen, camera.vector)
    

    def get_game_object_by_name(self, name):
        for y in self.layers:
            for x in y:
                if x.name == name:
                    return x
        raise KeyError(f'not has layer in {name}')
    
    @staticmethod
    def load(path):
        manger.layers = Layers()
        file = open(path, 'r')
        json_file :dict = json.loads(file.read())
        file.close()
        manger.load_game_object(json_file)
