import pygame
from ..event import Event

class Button(pygame.sprite.Sprite):
    
    def __init__(self, size, pos, string, color, image, click_image):
        super().__init__()
        self.size = size
        self.pos = pos
        self.text = pygame.font.Font().render(string, True, color)
        self.text_rect = self.text.get_rect()
        self.default_image = pygame.transform.scale(pygame.image.load(image), size)
        self.click_image = pygame.transform.scale(pygame.image.load(click_image), size)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.event = Event()
        self.is_pressing = False
        self.is_on = False
        self.active = True
        
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

            
    def update(self, active = False):
        if self.is_click():
            self.event.invoke()
        self.active = active
        if self.active:
            self.image.blit(self.text, self.text_rect)