import pygame
import color
from scene import SceneLoad

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        self.width,self.height = size
        self.screen = pygame.display.set_mode(size=size)
        SceneLoad(self.screen)
        self.is_running = True


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
    
    @SceneLoad.SceneChange
    def start(self):
        self.screen.fill(color.RED)
        self.create_text(str="Ai Defense Game")
        self.create_text(str="Press a key to play", size=20, center=((400, 400)))
        pygame.display.update()
        self.wait_key()

          
    def main(self):
        SceneLoad.Change_Scene
        while self.is_running:

            self.scene.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            pygame.display.update()

        pygame.quit() # 종료
        
    def game_over(self):
        if not self.is_running:
            return

if __name__ == "__main__" :
    game = AiDefenseGame(size=(800, 600))
    game.start()
    game.main()