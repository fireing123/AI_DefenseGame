from typing import List, Callable
import threading

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
    
    def invoke(self, *arg):
        for function in self.lisners:
            function(*arg)

class SharedThread:
    def __init__(self):
        self.condition = threading.Condition()
        self.is_ready = False
        self.plz_wait = False