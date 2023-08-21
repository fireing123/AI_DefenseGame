from typing import List, Callable

# 최적화 요구..

class Event:
    """
    event
    """
    def __init__(self):
        self.lisners : List[Callable]= []
    
    def __call__(self):
        self.invoke()
    
    def __len__(self):
        return len(self.lisners)
    
    def add_lisner(self, function : Callable):
        self.lisners.append(function)
    
    def invoke(self):
        for function in self.lisners:
            function()