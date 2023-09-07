import pygame
import xml.etree.ElementTree as xml

class SoundManger:
    def __init__(self):
        self.path = "D:/AI_DefenseGame/src/sound/sound.xml"
        docs = xml.parse(self.path)
        root = docs.getroot()
        self.music_dir = {}
        
        for child in root:
            att = child.attrib
            self.music_dir[att['name']] = pygame.mixer.Sound(att['path'])
