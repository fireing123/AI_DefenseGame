import json
import threading
import manger

class Story:
    
    def __init__(self, path, game):
        with open(path, 'r') as f:
            json_file = json.loads(f.read())
            self.json = json_file
            self.index = 0
            self.game = game

    def update(self):
        if self.index + 1 > len(self.json['story']):
            self.game.is_running = False
            return
        updated = self.json['story'][self.index]
        self.index += 1
        obj = manger.layers.get_game_object_by_name(updated['object'])
        motion = updated['motion']
        if motion[0] == 'm':
            obj.direction.x = int(motion[1:])
        elif motion[0] == 's':
            obj.say(motion[2:], int(motion[1]))
        threading.Timer(updated['wait'], self.update).start()