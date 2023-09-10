import os
import threading
import pygame
from pygame import time
from time import sleep
from typing import Dict, List, Tuple
import manger
from event import Event
from object import GameObject, Position
from sheet import SpriteSheet # color import
from animation import AnimationText # object

def image_load_to_scale(path, scale):
    return pygame.transform.scale(pygame.image.load(os.getcwd()+'/'+path), scale)

class UI(GameObject):
    
    def __init__(self, name):
        super().__init__(name, 4)

class Button(UI):
    """
    버튼이다. 클릭할수 있는듯하다...
    """
    def __init__(self, name, position : tuple[int, int], scale : tuple[int, int],
                text, default_image : str, click_image : str):
        super().__init__(name)
        self.default_image = image_load_to_scale(default_image, scale)
        self.click_image = image_load_to_scale(click_image, scale)
        self.image = self.default_image
        self.text = Text.instantiate(text)
        self.rect = self.image.get_rect()
        self.position = Position(*position)
        self.on_click = Event()
        self.is_pressing = False
        self.is_on = False

    def child_position(self):
        self.text.position = self.position

    @staticmethod
    def instantiate(json):
        return Button(
            json['name'],
            tuple(json['position']),
            tuple(json['scale']),
            json['text'],
            json['defaultImage'],
            json['clickImage']
        )
        
    def is_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            mouse_press = pygame.mouse.get_pressed()[0]
            
            if mouse_press:
                self.image = self.click_image
                self.is_on = not self.is_pressing
            else:
                self.image = self.default_image
    
            self.is_pressing = mouse_press
        return self.is_on

    def render(self, surface, camera):
        if self.visible:
            surface.blit(self.image, self.rect)
            
    def update(self, mod):
        if self.is_click():
            self.on_click.invoke()
            self.is_on = False
    
class SkillBox(UI):
    def __init__(self, name, position, skill_path):
        super().__init__(name)
        self.image = image_load_to_scale(skill_path, (32, 32))
        self.rect = self.image.get_rect()
        self.position = position
        
    def render(self, surface, camera):
        if self.visible:
            surface.blit(self.image, self.rect)
            
class Q(SkillBox):
    def __init__(self, name, position):
        super().__init__(name, position, './image/skill/bomb-skill.png')

    def update(self, mod):
        self.visible = manger.player.skill_q_ev 
    
    @staticmethod
    def instantiate(json: Dict):
        return Q(
            json['name'],
            json['position']
        )
    
class W(SkillBox):
    def __init__(self, name, position):
        super().__init__(name, position, './image/skill/bomb-skill.png')

    def update(self, mod):
        self.visible = manger.player.skill_w_ev
        
    @staticmethod
    def instantiate(json: Dict):
        return W(
            json['name'],
            json['position']
        )
        
class E(SkillBox):
    def __init__(self, name, position):
        super().__init__(name, position, './image/skill/bomb-skill.png')

    def update(self, mod):
        self.visible = manger.player.skill_e_ev    

    @staticmethod
    def instantiate(json: Dict):
        return E(
            json['name'],
            json['position']
        )

class ChatBox(UI):
    def __init__(self, name, text):
        super().__init__(name)
        chat_box = SpriteSheet('./image/chatBox/config.xml')
        self.visible = False
        self.open_image = chat_box['open']
        self.box_image  = chat_box['box']
        self.arrow_image = chat_box['arrow']
        self.close_image = chat_box['close']
        self.text = AnimaText.instantiate(text)
        self.open_rect = self.open_image.get_rect()
        self.arrow_rect = self.arrow_image.get_rect()
        self.close_rect = self.close_image.get_rect()
        self.box_rect = self.box_image.get_rect()
    
        
    def say(self, chat, time):
        manger.thread_connect.plz_wait = True
        self.time = time
        self.visible = True
        gox, goy = self.game_object.position
        gsx, gsy = self.game_object.image.get_size()
        self.position = (gox + gsx/2, goy - gsy/1.8)
        self.text.position = self.position
        loxy = self.text.start_animation(
            AnimationText.load(chat)
        )
        x, _ = self.position
        lox ,_ = loxy
        _ , boxy= self.box_image.get_size()
        self.box_image = pygame.transform.scale(self.box_image, (lox - x, boxy))
        thread = threading.Thread(target=self.sleep)
        thread.start()
        with manger.thread_connect.condition:
            manger.thread_connect.plz_wait = False
            manger.thread_connect.condition.notify()
        
    def sleep(self):
        sleep(self.time)
        self.visible = False
    
    def set_player(self, game_object):
        self.game_object : GameObject = game_object
    
    def update(self, mod):
        self.text.visible = self.visible
        gox, goy = self.game_object.rect_position
        gsx, gsy = self.game_object.image.get_size()
        self.position = (gox + gsx/3, goy - gsy/3)
        self.text.position = self.position
        x, y = self.position
        self.open_rect.bottomright = x, y + 5
        self.box_rect = self.box_image.get_rect()
        self.box_rect.bottomleft = self.open_rect.bottomright
        self.close_rect.bottomleft = self.box_rect.bottomright
        gx, gy = self.position
        self.arrow_rect.midtop = gx + 20, gy
    
    def render(self, surface : pygame.Surface, camera):
        if not self.visible: return
        surface.blit(self.open_image, self.open_rect)
        surface.blit(self.box_image, self.box_rect)
        surface.blit(self.close_image, self.close_rect)
        surface.blit(self.arrow_image, self.arrow_rect)
    
    
    @staticmethod
    def instantiate(json: Dict):
        return ChatBox(
            json['name'],
            json['AnimaText']
        )
 
class AnimaText(UI):
    
    def __init__(self, name, position : tuple, color : tuple, tick):
        super().__init__(name)
        self.index = 0
        self.len = 1
        self.last_update : int = 0
        self.tick = tick
        self.color = color
        self.animation = [([(pygame.Surface((0, 0)), pygame.Rect(0, 0, 0, 0))], 500)]
        self.images , _= self.animation[0]
        self.position = position
        self.local_position = position
        
    def start_animation(self, ani_text : AnimationText):
        result : List[Tuple] = []
        animat : List[Tuple] = []
        self.index = 0
        self.animation.clear()
        self.local_position = self.position
        for char, scale, tick in ani_text:
            font = pygame.font.Font('./font/Galmuri11.ttf', scale)
            text = font.render(char, True, self.color)
            rect = text.get_rect()
            
            x, _ = text.get_size()
            rect.bottomleft = self.local_position
            lx, ly = self.local_position
            self.local_position = lx + x, ly
            
            result.append((text, rect))
            new_result =  result.copy()
            animat.append((new_result, tick))
            
        self.animation = animat
        self.len = len(self.animation)
        return self.local_position

    def update(self, mod):
        if time.get_ticks() - self.last_update > self.tick:
            
            self.last_update = time.get_ticks()
            self.images, self.tick = self.animation[self.index]
            if self.len > self.index + 1:
                self.index += 1
    
    def render(self, surface, camera):
        if not self.visible: return
        for image, rect in self.images:
            surface.blit(image, rect)

    @property
    def position(self):
        return tuple(self.__position)

    @position.setter
    def position(self, value):
        self.__position = Position(*value)
        self.rect.center = self.position
        self.local_position = self.position
        for text, rect in self.images:
            x, _ = text.get_size()
            rect.bottomleft = self.local_position
            lx, ly = self.local_position
            self.local_position = lx + x, ly

    @staticmethod 
    def instantiate(json):
        return AnimaText(
            json['name'],
            json['position'],
            json['color'],
            500
        )
 
class Text(UI):
    def __init__(self, name, position, scale, string, color):
        super().__init__(name)
        self.font = pygame.font.Font('./font/Galmuri11.ttf', scale)
        self.set_text(string, color)
        self.rect = self.image.get_rect()
        self.__text = string
        self.__color = color
        self.position = position
        
    def render(self, surface, camera):
        surface.blit(self.image, self.rect)    
    
    @property
    def text(self):
        return self.__text
    
    @text.getter
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, value):
        self.__text = value
        self.setter()
        
    @property
    def color(self):
        return self.__color
    
    @color.getter
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, value):
        self.__color = value
        self.setter()
    
    def setter(self):
        self.set_text(self.__text, self.__color)

    @staticmethod
    def instantiate(text):
        return Text(
            text['name'],
            tuple(text['position']), 
            text['scale'],
            text['string'],
            text['color']
        )
        
    def update(self, mod):
        super().update(mod)

    def set_text(self, string, color):
        self.image = self.font.render(string, True, color)
        self.rect = self.image.get_rect(center=self.position)
        
class Bar(UI):
    def __init__(self, name, game_object, color, back_color = (30,30,30), height = 0):
        super().__init__(name)
        self.game_object : GameObject = game_object
        self.rect = pygame.Rect(0, 0, 100, 20)
        self.color = color
        self.back_color = back_color
        self.height = height
        self.max = 100
        self.now = 100

    def render(self,screen, camera):
        x = self.game_object.rect.centerx # x,y좌표 설정
        y = self.game_object.rect.top - self.height
        cx, cy = camera
        px, py = x- cx, y - cy - 5
        pygame.draw.rect(screen,self.back_color,[px-(self.rect[2]*0.9)/2,py-self.rect[3]/2-20,self.rect[2]*0.9,10])
        pygame.draw.rect(screen,self.color,[px-(self.rect[2]*0.9)/2,py-self.rect[3]/2-20,((self.rect[2]*0.9)/self.max)*self.now,10])
        
class HPbar(Bar):
    def __init__(self, name, game_object, color = (255, 0, 0), back_color=(30, 30, 30)):
        super().__init__(name, game_object, color, back_color)
        
    def update(self, mod):
        self.max = self.game_object.max_hp
        self.now = self.game_object.hp
