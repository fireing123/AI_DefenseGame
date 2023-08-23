import pygame
from object import GameObject
from animation import Animation
from animation import AnimationController
from ground import group

class Player(GameObject):
    
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 100
        self.animation_controller = AnimationController()
        self.image : pygame.Surface
        self.rect = self.image.get_rect()

        self.direction = pygame.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))
        
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
    def update(self):
        if pygame.sprite.spritecollideany(self, group):
            pass
        else:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0
            if keys[pygame.K_SPACE] and self.on_ground:
                self.jump()
        
        #gravity
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y
        
        #animation
        self.animation_controller.update()
    
    def jump(self):
        self.direction.y = self.jump_speed