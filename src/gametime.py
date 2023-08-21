from pygame.time import Clock

clock = Clock()

class GameTime:
    
    @staticmethod
    def tick(tick : int):
        delta_time =  clock.tick(tick)