import pygame
import xml.etree.ElementTree as xml
from typing import Dict

class SoundManger:
    def __init__(self):
        self.path = "./sound/sound.xml"
        docs = xml.parse(self.path)
        root = docs.getroot()
        self.music_dir : Dict[str, pygame.mixer.Sound] = {}
        self.bgm : Dict[str, pygame.mixer.Sound] = {}
        for child in root:
            att = child.attrib
            if att.get('type') == 'bgm':
                self.bgm[att['name']] = pygame.mixer.Sound(att['path'])
            else:
                self.music_dir[att['name']] = pygame.mixer.Sound(att['path'])

    def all_stop(self):
        for _, sound in self.music_dir.items():
            sound.stop()
        for _ , bgm in self.bgm.items():
            bgm.stop()

    def stop(self, sound):
            try:
                self.music_dir[sound].stop()
            except IndexError:
                print(IndexError)

    def __getitem__(self, index):
        return self.music_dir[index]