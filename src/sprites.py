import pygame
from typing import Dict
import xml.etree.ElementTree as xml

class SpriteSheet:
    def __init__(self, xml_path):
        docs = xml.parse(xml_path)
        root = docs.getroot()
        self.full_image = pygame.image.load(root.attrib['imagePath'])
        self.images : Dict = []
        for child in root:
            att = child.attrib
            left_top = int(att['x']), int(att['y'])
            width_height =  int(att['width']), int(att['height'])
            rect = pygame.Rect(left_top, width_height)
            self.images[att['name']] = pygame.transform.chop(self.full_image, rect)
        
    def __len__(self):
        return self.images.__len__()

    def __getitem__(self, index):
        return self.images[index]
    
    def __setitem__(self, index, value):
        self.images[index] = value
    
