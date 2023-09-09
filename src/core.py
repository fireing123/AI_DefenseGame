import os
from typing import Dict
import pygame
import time
from pygame import Surface
import manger
from object import GameObject

class InstallCore(GameObject):
    
    def __init__(self, name: str, postition):
        super().__init__(name)
        self.image = pygame.image.load(os.getcwd() + "/src/image/install_core.png")
        self.fack_rect = self.image.get_rect(center=postition)
        self.rect = pygame.Rect(0, 0, 500, 200)
        self.position = postition
        
    def core_event(self, event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if pygame.sprite.collide_rect(manger.player, self):

                    self.image = pygame.image.load(os.getcwd() + "/src/image/core.png")
                    def end():
                        time.sleep(10)
                        manger.game.is_running = False
                    import threading
                    threading.Thread(target=end).start()
    
    def render(self, surface: Surface, camera: tuple):
        if not self.visible: return
        cx, cy = camera
        rx, ry = self.fack_rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(self.image, self.rect_position)
       
    @staticmethod 
    def instantiate(json: Dict):
        return InstallCore(
            json['name'],
            json['position']
        )