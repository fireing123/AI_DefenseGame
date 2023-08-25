

class Camera: 
    __x =0
    __y =0
    
    @property
    @staticmethod
    def vector():
        return Camera.__x, Camera.__y
    
    @vector.getter
    @staticmethod
    def vector():
        return Camera.__x, Camera.__y
    
    @vector.setter
    @staticmethod
    def vector(value):
        Camera.__x, Camera.__y = value
    
    @property
    @staticmethod
    def x():
        return Camera.__x
    
    @x.getter
    @staticmethod
    def x():
        return Camera.__x
    
    @x.setter
    @staticmethod
    def x(value):
        Camera.__x = value
    
    @property
    @staticmethod
    def y():
        return Camera.__y
    
    @y.getter
    @staticmethod
    def y():
        return Camera.__y
    
    @y.setter
    @staticmethod
    def y(value):
        Camera.__y = value
