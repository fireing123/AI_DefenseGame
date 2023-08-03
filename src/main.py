import pygame
import color

class AiDefenseGame:
    
    def __init__(self, size=(500, 500), tick=60):
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        self.width,self.height = size
        self.screen = pygame.display.set_mode(size=size)
        self.is_running = True
        self.clock = pygame.time.Clock()
    
    def create_text(self, object_name=None , str="", size=50, color=color.WHITE, center=(400, 300)):
        font = pygame.font.Font(object_name, size=size)
        text = font.render(str, True, color)
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
        self.screen.fill((0, 0, 0))
        self.create_text(str="Ai Defense Game")
        self.create_text(str="Press a key to play", size=20, center=((400, 400)))
        pygame.display.update()
        self.wait_key()
        
                     
    def main(self):

        self.screen.fill(color.WHITE)
        while self.is_running:
            self.clock.tick(60)

            for event in pygame.event.get(): # 
                if event.type == pygame.QUIT:
                    self.is_running = False
            pygame.display.update()

        pygame.quit() # 종료
        
    def game_over(self):
        if not self.is_running:
            return
        



print("ani is real")

if __name__ == "__main__" :
    game = AiDefenseGame(size=(800, 600), tick=60)
    game.start()
    game.main()