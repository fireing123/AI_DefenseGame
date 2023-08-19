
from object import GameObject


class Enemy(GameObject):
    """
    """
    def __init__(self, layer=3):
        super().__init__(layer)

class Soldier(Enemy):
    """
    적군인 오브젝트 전진, 발사기능이 있음
    """
    
    