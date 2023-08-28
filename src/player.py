import pygame
from typing import Dict, List
#not import my module
import manger
from object import LivingObject
from camera import camera
#import module first
from animation import AnimationController, Animation # object
from sheet import SpriteSheet # color
from ground import Ground # object
from enemy import group as enemy_group, Enemy


class Player(LivingObject):
    
    
    
    def __init__(self, name: str, position):
        super().__init__(name, position)
        self.keys = {}
        get_width, get_height = manger.screen.get_size()
        self.width, self.height = get_width/2, get_height/2
        self.health = 100

        self.speed = 2

        self.jump_speed = -6
        idle_animation = SpriteSheet('src/image/ai/config.xml')
        self.animation_controller = AnimationController(
            Animation(idle_animation.items()),
            self
        )
        self.image : pygame.Surface = idle_animation['ai_1']
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mass = True

        self.on_ground = True
        
    def player_event(self, event : pygame.event.Event):
        
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
            if event.key == pygame.K_UP and self.on_ground:
                self.jump()
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False
    
    def update(self):  
        
        try:
            if self.keys[pygame.K_RIGHT]:
                self.direction.x = self.speed
            if self.keys[pygame.K_LEFT]:
                self.direction.x = -self.speed
            if self.keys[pygame.K_0]: 
                self.remove()
        except KeyError:
            pass
         
        super().update()

        collision : List[Enemy] = pygame.sprite.spritecollide(self, enemy_group, False)

        for collide in collision:
            if collide.attack_possible(self):
                collide.attack(self)
            else:
                collide.advance(self)
        if self.rect_position[0] > self.width * 0.85:
            camera.x += 1

        if self.rect_position[0] < self.width * 0.25:
            camera.x -= 1

        #animation 
        self.image = self.animation_controller.update()
    
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def on_collision_enter(self, collision : Ground):
        pass
    
    def on_trigger_enter(self):
        pass
        
    def jump(self):
        self.add_force(0, self.jump_speed)
        self.on_ground = False
    
    def render(self, surface, camera):
        super().render(surface, camera)
        
    @staticmethod
    def instantiate(json: Dict):
        return Player("super", json['position'])