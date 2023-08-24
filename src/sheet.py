import pygame
from typing import Dict
import color
import xml.etree.ElementTree as xml

class SpriteSheet:
    def __init__(self, xml_path):
        
        docs = xml.parse(xml_path)
        root = docs.getroot()
        self.full_image = pygame.image.load(root.attrib['imagePath'])
        self.images : Dict[str, pygame.Surface] = {}
        
        for child in root:
            att = child.attrib
            xywh = int(att['x']), int(att['y']), int(att['width']), int(att['height'])
            self.images[att['name']] = self.get_image(*xywh)
    
    def get_image(self, x, y, width, height) -> pygame.Surface:
        image = pygame.Surface((width, height))
        image.fill(color.RED)
        image.set_colorkey(color.RED)
        image.blit(self.full_image, (0, 0), (x, y, width, height))
        return image
    
    def __len__(self):
        return self.images.__len__()

    def __getitem__(self, index):
        return self.images[index]
    
    def __setitem__(self, index, value):
        self.images[index] = value
        
    def keys(self):
        return self.images.keys()
    
    def items(self):
        return self.images.items()