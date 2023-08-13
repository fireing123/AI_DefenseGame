import pygame
from . import color
from .scene import Scene, UI

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        self.width,self.height = size
        self.screen = pygame.display.set_mode(size=size)
        self.scene : Scene = Scene.load('src\level\main.json', self.screen)
        self.is_running = True

    
    def wait_key(self, what_key):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False
                if event.type == what_key:
                    waiting = False
    
    
    
    def start(self):
        self.scene.update()
        self.scene.draw()
        pygame.display.update()
        self.wait_key(pygame.KEYUP)

    def main(self):
        
        self.scene = self.scene.scene_change('src/level/laboratory.json')
        while self.is_running:
            self.scene.update()
            self.scene.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            pygame.display.update()

        pygame.quit() # 종료
        
    def game_over(self):
        if not self.is_running:
            return

if __name__ == "__main__" :
    game = AiDefenseGame(size=(1000, 800))
    game.start()
    game.main()