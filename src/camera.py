class Camera: 
    def __init__(self):
        self.__x = 0
        self.__y = 0
    
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