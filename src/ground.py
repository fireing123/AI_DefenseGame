import pygame
from object import GameObject

group = pygame.sprite.Group()

class Ground(GameObject):
    
    def __init__(self):
        group.add(self)