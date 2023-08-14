import pygame
from ..event import Event
from .object import Object

class Button(Object):
    
    def __init__(self, pos_x, pos_y, rot, scl_x, scl_y,
                text, default_image, click_image, parent=None,
                *children):
        super().__init__(pos_x, pos_y, rot, scl_x, scl_y, parent, *children)
        local_scale =tuple(self.transform.local_scale)
        self.default_image = pygame.transform.scale(pygame.image.load(default_image), local_scale)
        self.click_image = pygame.transform.scale(pygame.image.load(click_image), local_scale)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        x, y = local_scale
        self.text = Text(x//2, y//2, rot, scl_x ,text['string'], text['color'])
        self.event = Event()
        self.is_pressing = False
        self.is_on = False


    @staticmethod
    def load(button_json):
        x, y = tuple(button_json['position'])
        s, c = tuple(button_json['size'])
        return Button(
            x, y,
            button_json['rotation'],
            s, c,
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
        super().update()
        if self.is_click():
            self.event.invoke()
        
    def draw(self, screen : pygame.surface.Surface):
        screen.blit(self.image, self.rect)
        self.text.draw(screen)

class Text(Object):
    
    def __init__(self, pos_x, pos_y, rot, scl_x,
        string, color,
        parent=None, *children):
        super().__init__(pos_x, pos_y, rot, scl_x, 1, parent, *children)
        self.font = pygame.font.Font(None, int(self.transform.local_scale.x))
        self.image = self.font.render(string, True, color)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.center = self.transform.local_position
        
    @staticmethod
    def load(text):
        pos_x, pos_y = tuple(text['position'])
        rot = text['rotation']
        scale, _ = tuple(text['size'])
        return Text(
            pos_x, pos_y, rot, scale,
            text['string'],
            text['color']
        )
        
    def update(self):
        super().update()
        
    def draw(self, surface):
        super().draw(surface)
        
    def set_text(self, string, color):
        self.image = self.font.render(string, True, color)