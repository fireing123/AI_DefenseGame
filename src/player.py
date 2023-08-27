import pygame
from typing import Dict
#not import my module
import manger
from object import LivingObject
from camera import camera
#import module first
from animation import AnimationController # object
from sheet import SpriteSheet # color
from ground import group, Ground # object



class Player(LivingObject):
    
    
    
    def __init__(self, name: str, position):
        super().__init__(name, position)

        get_width, get_height = manger.screen.get_size()
        self.width, self.height = get_width/2, get_height/2
        self.health = 100

        self.speed = 2

        self.jump_speed = -6
        idle_animation = SpriteSheet('src/image/ai/config.xml')
        self.animation_controller = AnimationController(
            idle_animation.items(),
            self
        )
        self.image : pygame.Surface = idle_animation['ai_1']
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mass = False

        self.on_ground = True
        
    def player_event(self, event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.mass = False
            if event.key == pygame.K_RIGHT:
                self.add_force(self.speed)
            elif event.key == pygame.K_LEFT:
                self.add_force(-self.speed)
            if event.key == pygame.K_SPACE and self.on_ground:
                self.jump()
        if event.type == pygame.KEYUP and event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
            self.mass = True
    
    def update(self):   
        super().update()

        if self.rect_position[0] > self.width * 0.85:
            camera.x += 1

        if self.rect_position[0] < self.width * 0.25:
            camera.x -= 1

        #animation 
       # self.animation_controller.update()
    
    def on_collision_enter(self, collision : Ground):
        pass
        
    def jump(self):
        self.add_force(0, self.jump_speed)
        self.on_ground = False
    
    def render(self, surface, camera):
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(self.image, self.rect_position)
        
    @staticmethod
    def instantiate(json: Dict):
        return Player("super", json['position'])