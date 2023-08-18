
# 최적화 요구..

class Event:
    
    def __init__(self):
        self.lisners = []
    
    def __call__(self):
        self.invoke()
    
    def __len__(self):
        return len(self.lisners)
    
    def add_lisner(self, function):
        self.lisners.append(function)
    
    def invoke(self):
        for function in self.lisners:
            function()