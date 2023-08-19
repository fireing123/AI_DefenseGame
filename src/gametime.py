from pygame.time import Clock

clock = Clock()

class GameTime:
    
    @staticmethod
    def tick(tick):
        delta_time =  clock.tick(tick)