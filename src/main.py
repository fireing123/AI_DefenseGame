import pygame
# not import my module
import manger
import sys

from gametime import GameTime
from camera import camera

from scene import Scene

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        manger.game = self
        self.game_over = False
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        manger.screen = pygame.display.set_mode(size)
        manger.Layers.load('src\level\main.json')
        self.width,self.height  = size
        self.scene = Scene()
        self.is_running = True

    def start(self):
        
        waiting = True
        while waiting:
            manger.layers.update()
            manger.layers.render()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False
                    break
                if event.type == pygame.KEYUP:
                    waiting = False

    def prologue(self):
        pass

    def laboratory(self):
        
        self.scene.darkening_scene()
        manger.Layers.load('src/level/laboratory.json')
        # awake
        button = manger.layers.get_game_object_by_name("enter")
        player = manger.layers.get_game_object_by_name('super')
        ani = manger.layers.get_game_object_by_name("chatbox")
        button.event.add_lisner(lambda : ani.say('src/chat/test.json', 5))
        ani.set_player(player)
        core = manger.layers.get_game_object_by_name("core")
        core.set_world(self)
        #end
        self.scene.brightening_scene()

        while self.is_running:
            GameTime.tick(60)
            
            for event in pygame.event.get():
                player.player_event(event)
                if event.type == pygame.QUIT:
                    self.is_running = False

            manger.layers.update()
            manger.layers.render()
            pygame.display.update()
            
        if self.game_over:
            print("game_over")
            pygame.quit()
            sys.exit()
            
    def mountain(self):
        self.scene.darkening_scene()
        manger.Layers.load('src/level/laboratory.json')
        # awake
        
        #end
        self.scene.brightening_scene()
        
        while self.is_running:
            GameTime.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            manger.layers.update()
            manger.layers.render()
            pygame.display.update()
            
        if self.game_over:
            pygame.quit()
            sys.exit()
        
    def last_laboratory(self):
        self.scene.darkening_scene()
        manger.Layers.load('src/level/laboratory.json')
        # awake
        
        #end
        self.scene.brightening_scene()
        
        while self.is_running:
            GameTime.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            manger.layers.update()
            manger.layers.render()
            pygame.display.update()
            
        if self.game_over:
            pygame.quit()
            sys.exit()
                
if __name__ == "__main__" :
    game = AiDefenseGame(size=(1000, 800))
    game.start()
    game.prologue()
    game.laboratory()
    game.mountain()
    game.last_laboratory()
    pygame.quit() # 종료