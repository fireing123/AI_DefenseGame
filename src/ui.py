import pygame
from typing import Dict, List, Tuple
from event import Event
from object import GameObject
from sheet import SpriteSheet
from animation import AnimationText
from time import sleep
from pygame import time

def image_load_to_scale(path, scale):
    return pygame.transform.scale(pygame.image.load(path), scale)


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
        self.rect.center = position
        self.event = Event()
        self.is_pressing = False
        self.is_on = False

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

    def render(self, surface):
        surface.blit(self.image, self.rect)
        self.text.render(surface)
            
    def update(self):
        if self.is_click():
            self.event.invoke()
            self.is_on = False
    

class ChatBox(UI):
    def __init__(self, name, position, text, game_object):
        super().__init__(name)
        chat_box = SpriteSheet('src/image/chatBox/config.xml')
        #self.game_object = game_object
        self.open_image = chat_box['open']
        self.box_image  = chat_box['box']
        self.arrow_image = chat_box['arrow']
        self.close_image = chat_box['close']
        self.text = AnimaText.instantiate(text)
        self.position = position
        self.open_rect = self.open_image.get_rect()
        self.arrow_rect = self.arrow_image.get_rect()
        self.close_rect = self.close_image.get_rect()
        self.box_rect = self.box_image.get_rect()
        self.arrow_rect.center = (400, 200)
        self.open_rect.center = (500, 200)
        self.close_rect.center = (550,200)
        self.box_rect.center = (600, 200)
        
    def say(self, chat):
        xy, loxy = self.text.start_animation(
            AnimationText.load(chat)
        )
        #x, y = xy
        #lox ,_ = loxy
        #self.open_rect.bottomright = x, y + 5
        #_ , boxy= self.box_image.get_size()
        #self.box_image = pygame.transform.scale(self.box_image, (lox - x, boxy))
        #self.box_rect = self.box_image.get_rect()
        #self.box_rect.bottomleft = self.open_rect.bottomright
        #self.close_rect.bottomleft = self.box_rect.bottomright
        ##gx, _ = self.game_object.position
        #gx = 500
        #self.arrow_rect.midtop = gx, y - 2
    
    def update(self):
        self.text.update()
    
    def render(self, surface : pygame.Surface):
        surface.blit(self.open_image, self.open_rect)
        surface.blit(self.box_image, self.box_rect)
        surface.blit(self.close_image, self.close_rect)
        surface.blit(self.arrow_image, self.arrow_rect)
        self.text.render(surface)
    
    @staticmethod
    def instantiate(json: Dict):
        return ChatBox(
            json['name'],
            json['position'],
            json['AnimaText'],
            None
        )
 
class AnimaText(UI):
    
    def __init__(self, name, position : tuple, color : tuple, tick):
        super().__init__(name)
        self.index = 0
        self.len = 1
        self.last_update : int = 0
        self.tick = tick
        self.position = position
        self.local_position = position
        self.color = color
        self.animation = [([(pygame.Surface((50, 50)), pygame.Rect(0, 0, 0, 0))], 500)]
        self.images , _= self.animation[0]
        
    def start_animation(self, ani_text : AnimationText):
        
        result : List[Tuple] = []
        animat : List[Tuple] = []
        self.index = 0
        self.animation.clear()
        self.local_position = self.position
        for char, scale, tick in ani_text:
            font = pygame.font.Font('src/font/Galmuri11.ttf', scale)
            text = font.render(char, True, self.color)
            rect = text.get_rect()
            rect.bottomleft = self.local_position
            x, _ = font.size(char)
            lx, ly = self.local_position
            self.local_position = lx + x, ly
            result.append((text, rect))
            new_result =  result.copy()
            animat.append((new_result, tick))
        self.animation = animat
        self.len = len(self.animation)
        return self.position, self.local_position

    def update(self):
        if time.get_ticks() - self.last_update > self.tick:
            
            self.last_update = time.get_ticks()
            self.images, self.tick = self.animation[self.index]
            if self.len != self.index + 1:
                self.index += 1
    
    def render(self, surface):
        for image, rect in self.images:
            surface.blit(image, rect)

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
        self.font = pygame.font.Font('src/font/Galmuri11.ttf', scale)
        self.set_text(string, color)
        self.rect = self.image.get_rect()
        self.__text = string
        self.__color = color
        self.position = position
        self.rect.center = position
        
    def render(self, surface):
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
        self.rect.center = self.position
        
    @staticmethod
    def instantiate(text):
        return Text(
            text['name'],
            tuple(text['position']), 
            text['scale'],
            text['string'],
            text['color']
        )
        
    def update(self):
        super().update()

    def set_text(self, string, color):
        self.image = self.font.render(string, True, color)
        self.rect = self.image.get_rect()
        
class HPbar(UI):
    def __init__(self, name, position : tuple[int, int]):
        super.__init__(name)
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = position

    def render(self, surface):
        pass


#    def render(self, surface):
 #       surface.blit(self.image, self.rect)    

#    def render(self,sprite_image,position : list,hp,maxhp,Surface,type): #순서대로 이미지,위치[x,y],hp,maxhp,표면,타입
#        self.x , self.y = position[0], position[1] # x,y좌표 설정
#        self.rect = sprite_image.get_rect(center = (self.x, self.y)) #중심 xy기준으로 사각형얻기
#        self.hp = hp
#        self.maxhp = maxhp
#
#        if type == 1: #ai를 타입1로
#            color = (0,0,255)
#        elif type == 2: #enemy를 타입2로
#            color = (255,0,0)
#
#
#        pygame.draw.rect(Surface,(30,30,30),[self.rect.centerx-(self.rect[2]*1.1)/2,self.rect.top-25,self.rect[2]*1.1,10])
#        pygame.draw.rect(Surface,color,[self.rect.centerx-(self.rect[2]*1.1)/2,self.rect.top-25,((self.rect[2]*1.1)/maxhp)*hp,10])

#HPbar코드 입맛대로 뜯어고치고 재탕해둘것

# 거의 방치됨
        
#HP = u'▀▀▀▀▀▀▀▀▀▀'
#class EnemyHP(Sprite):
#    
#    def __init__(self, position, rot, scale, 
#                image_path, hp,
#                parent, children=[]):
#        new_child = children
#        new_hp = hp
#        pos_x, pos_y = parent.position
#        _ , height = parent.scale
#        new_hp['postion'] = (pos_x, pos_y + height//2 + 25)
#
#        new_child.append(Text.load(new_hp))
#        super().__init__(position, rot, scale, parent, new_child)
#        self.image = image_load_to_scale(image_path)
