import threading
from time import sleep

class Camera: 
    def __init__(self):
        self.__x = 0
        self.__y = 0
    
    def shiver(self):
        def real_shiver():
            self.vector = (self.x + 5, self.y + 5)
            sleep(0.2)
            self.vector = (self.x - 5, self.y - 5)
            sleep(0.2)
        shiver = threading.Thread(target=real_shiver)
        shiver.start()        

    def earthquake(self):
        def real_earthquake():
            self.vector = (self.x, self.y + 5)
            sleep(0.2)
            self.vector = (self.x - 5, self.y)
            sleep(0.2)
            self.vector = (self.x + 5, self.y)
            sleep(0.2)
            self.vector = (self.x, self.y - 5)
            sleep(0.2)
        earthquake = threading.Thread(target=real_earthquake)
        earthquake.start()
        
    def launch(self, direction):
        def real_launch(dir):
            self.vector = self.x - dir[0] / 10, self.y - dir[1] / 10
            sleep(0.2)
            self.vector = self.x + dir[0] / 50, self.y + dir[1] / 50
            sleep(0.2)
            self.vector = self.x + dir[0] / 50, self.y + dir[1] / 50
            sleep(0.2)
            self.vector = self.x + dir[0] / 50, self.y + dir[1] / 50
            sleep(0.2)
            self.vector = self.x + dir[0] / 50, self.y + dir[1] / 50
            sleep(0.2)
            self.vector = self.x + dir[0] / 50, self.y + dir[1] / 50
        launch = threading.Thread(target=real_launch, args=(direction))
        launch.start()
    
    def move_camera(self, x, y):
        self.vector = (x, y)
    
    @property
    def vector(self):
        return self.__x, self.__y
    
    @vector.getter
    def vector(self):
        return self.__x, self.__y
    
    @vector.setter
    def vector(self, value):
        self.__x, self.__y = value
    
    @property
    def x(self):
        return self.__x
    
    @x.getter
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, value):
        self.__x = value
    
    @property
    def y(self):
        return self.__y
    
    @y.getter
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, value):
        self.__y = value

camera = Camera()