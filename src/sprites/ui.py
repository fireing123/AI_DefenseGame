from typing import Optional
import pygame
from ..event import Event


class Button(pygame.sprite.Sprite):
    
    def __init__(self, size : tuple[int, int], pos, text, image, click_image):
        super().__init__()
        self.size = size
        self.default_image = pygame.transform.scale(pygame.image.load(image), size)
        self.click_image = pygame.transform.scale(pygame.image.load(click_image), size)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        x, y = size
        
        self.text = Text(None, (x//2, y//2), 100, text['string'], text['color'])
        
        self.event = Event()
        self.is_pressing = False
        self.is_on = False

    @staticmethod
    def load(button_json):
        return Button(
            tuple(button_json['size']),
            tuple(button_json['position']),
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

            
    def update(self):
        if self.is_click():
            self.event.invoke()
        
    def draw(self, screen : pygame.surface.Surface):
        screen.blit(self.image, self.rect)
        
        screen.blit(self.text.text, self.text.rect)

class Text(pygame.font.Font):
    
    def __init__(self, name, position, size, string, color):
        super().__init__(name, size)
        self.text = self.render(string, True, color)
        self.color = color
        self.rect = self.text.get_rect()
        self.rect.center = position
        
    @staticmethod
    def load(text):
        return Text(
            None,
            text['position'],
            text['size'],
            text['string'],
            text['color']
        )
        
    def set_text(self, string, color):
        self.text = self.render(string, True, color)