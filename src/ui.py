import pygame
from pygame.sprite import Sprite
from event import Event
from object import GameObject



def image_load_to_scale(path, scale):
    return pygame.transform.scale(pygame.image.load(path), scale)

class Button(GameObject):
    """
    버튼이다. 클릭할수 있는듯하다...
    """
    def __init__(self, position : tuple[int, int], scale : tuple[int, int],
                text, default_image : str, click_image : str):
        super().__init__()
        self.default_image = image_load_to_scale(default_image, scale)
        self.click_image = image_load_to_scale(click_image, scale)
        self.image = self.default_image
        self.text = Text.load(text)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.event = Event()
        self.is_pressing = False
        self.is_on = False

    @staticmethod
    def load(button_json):
        return Button(
            tuple(button_json['position']),
            tuple(button_json['size']),
            button_json['text'],
            button_json['defaultImage'],
            button_json['clickImage']
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
        


class Text(GameObject):
    def __init__(self, position, scale, string, color):
        super().__init__()
        self.font = pygame.font.Font('src/font/Galmuri11.ttf', scale)
        self.set_text(string, color)
        self.rect = self.image.get_rect()
        self.__text = string
        self.__color = color
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
        
    @staticmethod
    def load(text):
        return Text(
            tuple(text['position']), 
            text['size'],
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
