import pygame

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        pygame.init()
        self.screen = pygame.display.set_mode(size=size)
        self.is_running = True
    
    def create_text(self, object_name=None , str="", size=50, color=(0, 0, 0), center=(250, 250)):
        font = pygame.font.Font(object_name, size=size)
        text = font.render(text=str, antialias=True, color=color)
        text_rect = text.get_rect()
        text_rect.center = center
        self.screen.blit(text, text_rect)
    
    def wait_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False
                if event.type == pygame.KEYUP:
                    waiting = False
    
    def start(self):
        pass
                     
    def main(self):

        while self.is_running:


            for event in pygame.event.get(): # 
                if event.type == pygame.QUIT:
                    is_running = False

        pygame.quit() # 종료



print("ani is real")

if __name__ == "__main__" :
    game = AiDefenseGame()
    game.start()