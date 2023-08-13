import pygame
from .transform import Transform
from pygame.math import Vector2


class object(pygame.sprite.Sprite):
    
    def __init__(self, group,pos_x, pos_y, rot_x, rot_y, scl_x, scl_y, parent=None, *children):
        super().__init__(group)
        self.transform = Transform(
            Vector2(pos_x, pos_y),
            Vector2(rot_x, rot_y),
            Vector2(scl_x, scl_y),
            parent,
            list(children)
        )


    def draw(self, surface):
        surface.blit(self.image, self.rect)
    