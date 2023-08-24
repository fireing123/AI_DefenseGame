from typing import Dict
import pygame
import time
from object import GameObject
from animation import Animation
from animation import AnimationController
from ground import group, Ground

class Player(GameObject):
    
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 100
        #self.animation_controller = AnimationController()
        self.image : pygame.Surface = pygame.Surface((100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 1
        self.gravity = 0.02
        self.jump_speed = -3
       
        
        self.mass = False
        self.facing_right = True
        self.on_ground = True
        
    def player_event(self, event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.mass = False
            if event.key == pygame.K_RIGHT:
                self.direction.x = self.speed
                self.facing_right = True
            elif event.key == pygame.K_LEFT:
                self.direction.x = -self.speed
                self.facing_right = False
            if event.key == pygame.K_SPACE and self.on_ground:
                self.jump()
        if event.type == pygame.KEYUP and event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
            self.mass = True
    
    def update(self):   
        collide = pygame.sprite.spritecollideany(self, group)
        if collide != None:
            self.on_collision_enter(collide)

            self.friction = 0.4
        else:
            self.direction.y += self.gravity
            self.friction = 1
    
        self.rect.y += self.direction.y
        self.rect.x += self.direction.x
        
        if self.mass:
            self.direction.x *= self.friction
            if abs(self.direction.x) < 0.1:
                self.direction.x = 0

        #animation 
       # self.animation_controller.update()
    
    def on_collision_enter(self, collision : Ground):
        cox, coy = collision.rect.size
        cox, coy = cox/2, coy/2
        if self.rect.bottom < collision.rect.top + coy:
            self.rect.bottom = collision.rect.top
            self.direction.y = 0
        else:
            self.direction.y += self.gravity
            if self.rect.top > collision.rect.bottom - coy:
                #bottom
                self.rect.top = collision.rect.bottom
                self.direction.y = 0
            elif self.rect.left < collision.rect.right + cox:
                #right
                self.rect.left = collision.rect.right
                self.direction.x = 0
            elif self.rect.right > collision.rect.left - cox:
                #left
                self.rect.right = collision.rect.left
                self.direction.x = 0
    
    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False
        
    def render(self, surface):
        surface.blit(self.image, self.rect)
        
    @staticmethod
    def instantiate(json: Dict):
        return Player("super")