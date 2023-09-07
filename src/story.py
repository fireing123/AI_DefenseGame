import json
import threading
import time
import manger

class Story:
    
    def __init__(self, path, game):
        with open(path, 'r') as f:
            json_file = json.loads(f.read())
            self.json = json_file
            self.index = 0
            self.game = game
            self.stroy = path

    def update(self):
        if self.stroy != self.game.story: return
        if self.index + 1 > len(self.json['story']):
            self.game.is_running = False
            return
        updated = self.json['story'][self.index]
        self.index += 1
        try:
            global obj
            obj = manger.layers.get_game_object_by_name(updated['object'])
        except KeyError:
            print("story except")
            return
        motion : str = updated['motion']
        args = motion.split(',')
        if args[0] == 'v':
            obj.direction.x = int(args[1])
        elif args[0] == 'w':
            def work(sec, speed):
                micro = sec / 100
                for i in range(sec*100):
                    time.sleep(micro)
                    obj.direction.x = speed
            threading.Thread(target=work, args=(int(args[1]), int(args[2]))).start()
        elif args[0] == 's':
            obj.say(args[2], int(args[1]))
        elif args[0] == 'a':# attack func 
            obj.attack()
        elif args[0] == 'j': # jump func
            obj.direction.y = int(args[1])
        elif args[0] == 'd': # damge func
            obj.hp -= int(args[1])
        threading.Timer(updated['wait'], self.update).start()
        
    def quit(self):
        self.running = False