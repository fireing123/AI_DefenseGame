import pygame
import math
import manger
from pygame.sprite import Sprite
from pygame import Surface, Rect
from typing import Dict
from animation import AnimationController, Animation
from sheet import SpriteSheet # color

class Component:
    

    def start(self):
        pass
    
    def on_collision_enter(self, collision):
        pass
    
    def on_mouse_pressed(self):
        pass
    
    def update(self):
        pass
    
    def render(self, surface : Surface, camera : tuple):
        pass
    
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __len__(self):
        return 2
    
    
    def __add__(self, other):
        return self.__class__(
            self.x + other.x,
            self.y + other.y
        )

    def __iadd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return self.__class__(
            self.x - other.x,
            self.y - other.y
        )
        
    def __isub__(self, other):
        return self.__sub__(other)
        
    def __mul__(self, other):
        return self.__class__(
            self.x * other.x,
            self.y * other.y
        )
    
    def __imul__(self, other):
        return self.__mul__(other)
        
    def __div__(self, other):
        return self.__class__(
            self.x / other.x,
            self.y / other.y
        )
        
    def __idiv__(self, other):
        return self.__div__(other)
 
class GameObject(Sprite, Component):
    """
    기본 오브젝트
    """
          
    def __init__(self, name : str, layer = 3):
        Sprite.__init__(self)
        self.rect_position = (0, 0)
        self.layer_int = layer
        self.image : Surface
        self.rect = Rect(0,0,0,0)
        self.name = name
        self.__position = Position(0, 0)
        self.visible = True
        manger.layers.add(self)

    def remove(self):
        manger.layers.remove(self)
        self = None


    @property
    def position(self):
        return tuple(self.__position)

    @position.getter
    def position(self):
        return tuple(self.__position)
    
    @position.setter
    def position(self, value):
        self.__position = Position(*value)
        self.rect.center = self.position

    def render(self, surface: Surface, camera: tuple):
        if not self.visible: return
        cx, cy = camera
        rx, ry = self.rect.topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(self.image, self.rect_position)

    @staticmethod
    def instantiate(json : Dict):
        pass
        

class MoveObject(GameObject):
    
    
    def __init__(self, name):
        super().__init__(name)
        self.gravity = 0.08
        self.direction = pygame.Vector2(0, 0)
        self.on_ground = False
        self.friction = 0.6
        self.air_friction = 0.99
        self.mass = True
        self.rect : pygame.Rect
        
    def update(self):
        
        self.direction.y += self.gravity
        
        self.collision = pygame.sprite.spritecollide(self, manger.ground_group, False)
        if self.mass:
            self.direction.x *= self.friction
            if abs(self.direction.x) < 0.1:
                self.direction.x = 0    
        if self.collision:
            for collide in self.collision:
                cox, coy = collide.rect.size
                cox, coy = cox/2, coy/2
                if self.rect.bottom < collide.rect.top + coy:
                    self.rect.bottom = collide.rect.top + 1
                    self.direction.y = self.cut_minus(self.direction.y)
                    self.on_ground = True
                else:
                    self.direction.y += self.gravity
                    if self.rect.top > collide.rect.bottom - coy:
                        #bottom
                        self.rect.top = collide.rect.bottom
                        self.direction.y = self.cut_plus(self.direction.y)
                    elif self.rect.left > collide.rect.right - 5:
                        #right
                        self.rect.left = collide.rect.right
                        self.direction.x = 0
                    elif self.rect.right < collide.rect.left + 5:
                        #left
                        self.rect.right = collide.rect.left
                        self.direction.x = 0
                self.on_collision_enter(collide)
        else:
            self.friction = self.air_friction
        self.position = self.rect.center
        self.position += self.direction
        
    def cut_plus(self, num):
        if num < 0:
            return 0
        else:
            return num
    
    def cut_minus(self, num):
        if num > 0:
            return 0
        else:
            return num
        
    def add_force(self, x=0, y=0):
        self.direction += pygame.Vector2((x, y))

class LivingObject(MoveObject):
    
    def __init__(self, name, position, xml_path):
        super().__init__(name)
        self.__hp : int = 100
        self.max_hp : int = 100
        self.recognition_range = pygame.Rect((0, 0), (400, 400))
        
        idle_animation = SpriteSheet(xml_path)
        self.animation_controller = AnimationController(
            Animation(idle_animation.items()),
            self
        )
        self.image : pygame.Surface = idle_animation['default']
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.position = position
        
        self.hp_bar = manger.HPbar(name+"hpBar", self)
        
    def update(self):
        super().update()
        if self.direction.x > 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def destroy(self):
        self.hp_bar.remove()
        del self.hp_bar
     
    def look_angle(self, vector):
        a_vector = pygame.Vector2(*self.position)
        b_vector = pygame.Vector2(*vector)
        distance = a_vector.distance_to(b_vector)
        vec = b_vector - a_vector
        vec /= distance
        return vec
     
    @property
    def hp(self):
        return self.__hp
    
    @hp.setter
    def hp(self, value):
        self.__hp = value
        if self.__hp < 0:
            self.destroy()
            self.remove()
        elif self.max_hp < self.hp:
            self.__hp = self.max_hp
            
    @property
    def position(self):
        return tuple(self.__position)

    @position.getter
    def position(self):
        return tuple(self.__position)
    
    @position.setter
    def position(self, value):
        self.__position = Position(*value)
        self.rect.center = self.position
        self.recognition_range.center = self.position
