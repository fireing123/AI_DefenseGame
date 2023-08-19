import pygame

class GameTime:
    clock = pygame.time.Clock()
    delta_time = clock.tick(60)