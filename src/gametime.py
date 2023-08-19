import pygame

class GameTime:
    clock = pygame.time.Clock()
    delta_time = clock.tick(60)
    def tick(self, int):
        self.clock.tick(int)