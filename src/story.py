import json

class Story:
    
    def __init__(self, path):
        with open(path, 'r') as f:
            json_file = json.loads(f.read())
            self.json = json_file
        