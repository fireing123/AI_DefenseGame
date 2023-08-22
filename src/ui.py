import pygame
from event import Event
from object import GameObject
from sheet import SpriteSheet
from animation import Animation
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
    def __init__(self):
        super().__init__()
        chat_box = SpriteSheet('src/image/chatBox/config.xml')
        self.open_image = chat_box['open']
        self.box_image = chat_box['box']
        self.arrow_image = chat_box['arrow']
        self.close_image = chat_box['close']
        
    def say(self, text):
        pass

class StringAnimation:
    pass

class AnimaText(UI):
    
    def __init__(self, name, position : tuple, color : tuple, tick):
        super().__init__(name)
        self.index = 0
        self.len = 0
        self.last_update : int = 0
        self.tick = tick
        self.position = position
        self.local_position = position
        self.color = color
        self.animation = [([pygame.Surface((50, 50))], 500)]
    
    def start_animation(self, string_anima):
        
        result = []
        animat = []
        self.animation.clear()
        for char, scale, tick in StringAnimation:
            font = pygame.font.Font('src/font/Galmuri11.ttf', scale)
            text = font.render(result, True, self.color)
            rect = text.get_rect()
            _, y = font.size(char)
            lx, ly = self.local_position
            self.local_position = lx, ly+y
            rect.topleft = self.local_position
            result.append((text, rect))
            animat.append(result)
        self.animation = animat

    def update(self):
        if time.get_ticks() - self.last_update > self.tick:
            if self.len <= self.index:
                ims, t = self.animation[self.index]

            self.last_update = time.get_ticks()
            images, tick = self.animation[self.index]
            self.index += 1
            self.tick = tick
        return 
    
    def render(self, surface):
        surface.blits()
       
    @staticmethod 
    def instantiate(json):
        return AnimaText(
            json['name'],
            json['position'],
            json['scale'],
            json['color']
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
