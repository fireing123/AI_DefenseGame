import pygame
from .transform import Transform, Empty
from pygame.math import Vector2


class Object(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, rot, scl_x, scl_y, parent=None, *children):
        super().__init__()
        self.image : pygame.Surface
        self.rect : pygame.rect.Rect
        if parent == None:
            new_parent = Empty
        self.transform = Transform(
            Vector2(pos_x, pos_y),
            rot,
            Vector2(scl_x, scl_y),
            new_parent,
            list(children)
        )

    def update(self):
        self.image = pygame.transform.scale(self.image, self.transform.local_scale)
        self.image = pygame.transform.rotate(self.image, self.transform.local_rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.transform.local_position
        


    def draw(self, surface):
        surface.blit(self.image, self.rect)
    