from background import BackGround
from object import GameObject
from ui import Button, Text


def background_load(json, size):
    return BackGround(size, json)

class Layers:
    """
    전체 오브젝트를 포함하고
    오브젝트의 공통 함수를 실행합니다.
    """
    def __init__(self):
        self.layers : list[list[GameObject]] = [[],[],[],[],[]]
       
    def add(self,game_object: GameObject):
        layer_int = game_object.layer_int
        layer = self.layers[layer_int]
        layer.append(game_object)
         
    def absorb(self, list : list[GameObject]):
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
