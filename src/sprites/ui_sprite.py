import pygame

class Button(pygame.sprite.Sprite):
    
    def __init__(self, size, pos, string, color, image, click_image):
        super().__init__()
        self.size = size
        self.pos = pos
        self.text = pygame.font.Font().render(string, True, color)
        self.default_image = pygame.image.load(image)
        self.click_image = pygame.image.load(click_image)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.is_pressed = False
        
    def is_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.is_pressed = pygame.mouse.get_pressed()[0]
            
        
    def update(self):
        if self.is_click():
            self.image = self.click_image
        else:
            self.image = self.default_image
        self.image.blit(self.text)