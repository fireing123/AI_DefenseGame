import pygame
from . import color
from .scene import Scene

# 패르세우스의 배

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        self.width,self.height = size
        self.screen = pygame.display.set_mode(size=size)
        self.scene : Scene = Scene.load('src\level\main.json', self.screen)
        self.is_running = True

    def start(self):
        
        waiting = True
        while waiting:
            self.scene.update()
            self.scene.render()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def main(self):
        
        self.scene = self.scene.scene_change('src/level/laboratory.json')
        while self.is_running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    
            self.scene.update()
            self.scene.render()
            pygame.display.update()
            
        pygame.quit() # 종료
        
if __name__ == "__main__" :
    game = AiDefenseGame(size=(1000, 800))
    game.start()
    game.main()