import pygame
from typing import List


class SpriteSheet:
    def __init__(self, xml_path):
        self.full_image = pygame.image.load("")
        self.images : List[pygame.Surface] = []
        for rect in "":
            self.images += pygame.transform.chop(self.full_image, rect)
            
        
    def __len__(self):
        return self.images.__len__()

    def __getitem__(self, index):
        return self.images[index]
    
    