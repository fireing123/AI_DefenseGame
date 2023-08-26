import pygame
from typing import Dict
#not import my module
import manger
from object import GameObject
from camera import camera
#import module first
from animation import AnimationController # object
from sheet import SpriteSheet # color
from ground import group, Ground # object



class Player(GameObject):
    
    
    
    def __init__(self, name: str, position):
        super().__init__(name)

        get_width, get_height = manger.screen.get_size()
        self.width, self.height = get_width/2, get_height/2
        self.health = 100
        self.direction = pygame.Vector2(0, 0)
        self.speed = 2
        self.gravity = 0.08
        self.jump_speed = -6
        idle_animation = SpriteSheet('src/image/ai/config.xml')
        self.animation_controller = AnimationController(
            idle_animation.items(),
            self
        )
        self.image : pygame.Surface = idle_animation['ai_1']
        self.rect = self.image.get_rect()
        self.mass = False

        self.on_ground = True
        
    def player_event(self, event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.mass = False
            if event.key == pygame.K_RIGHT:
                self.direction.x = self.speed
            elif event.key == pygame.K_LEFT:
                self.direction.x = -self.speed

            if event.key == pygame.K_SPACE and self.on_ground:
                self.jump()
        if event.type == pygame.KEYUP and event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
            self.mass = True
    
    def update(self):   
        collison = pygame.sprite.spritecollide(self, group, False)
        
        self.direction.y += self.gravity
        
        if self.mass:
            self.direction.x *= self.friction
            if abs(self.direction.x) < 0.1:
                self.direction.x = 0
        
        if collison != None:
            for collide in collison:
                self.on_collision_enter(collide)

            self.friction = 0.4
        else:
            self.friction = 0.5
        self.position = self.rect.center
        self.position += self.direction

        if self.rect_position[0] > self.width * 0.85:
            camera.x += 1

        if self.rect_position[0] < self.width * 0.25:
            camera.x -= 1

        #animation 
       # self.animation_controller.update()
    
    def on_collision_enter(self, collision : Ground):
        cox, coy = collision.rect.size
        cox, coy = cox/2, coy/2
        if self.rect.bottom < collision.rect.top + coy:
            self.rect.bottom = collision.rect.top + 1
            self.direction.y = self.mn_numbrt(self.direction.y)
            self.on_ground = True
        else:
            self.direction.y += self.gravity
            if self.rect.top > collision.rect.bottom - coy:
                #bottom
                self.rect.top = collision.rect.bottom
                self.direction.y = self.process_number(self.direction.y)
            elif self.rect.left > collision.rect.right - 5:
                #right
                self.rect.left = collision.rect.right
                self.direction.x = 0
            elif self.rect.right < collision.rect.left + 5:
                #left
                self.rect.right = collision.rect.left
                self.direction.x = 0
        
    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False
    
    def process_number(self, num):
        if num < 0:
            return 0
        else:
            return num
    
    def mn_numbrt(self, num):
        if num > 0:
            return 0
        else:
            return num
    
    def render(self, surface, camera):
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(self.image, self.rect_position)
        
    @staticmethod
    def instantiate(json: Dict):
        return Player("super", json['position'])