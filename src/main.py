import pygame
# not import my module
import manger
import sys

from gametime import GameTime
from camera import camera
from story import Story
from scene import Scene

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        manger.game = self
        self.game_over = False
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        manger.screen = pygame.display.set_mode(size)
        manger.Layers.load('src/level/main.json')
        self.width,self.height  = size
        self.scene = Scene()
        self.is_running = True
        self.checkpoint = None
    def start(self):
        
        waiting = True
        while waiting:
            manger.layers.update()
            manger.layers.render()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    waiting = False
    

    
    def over(self):
        manger.screen.fill((0, 0, 0))
        manger.layers.clear()
        manger.Text("over", (500, 400), 50, "Game Over", (255, 255, 255))
        manger.layers.render()
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    waiting = False
        self.is_running = True

    def prologue(self):
        self.scene.darkening_scene()
        manger.Layers.load('src/level/prologue.json')
        manger.layers.mod = 'story'
        stroy = Story('src/story/prologue.json', self)
        player = manger.layers.get_game_object_by_name('player')
        ani = manger.layers.get_game_object_by_name("playerChat")
        skip : manger.Button = manger.layers.get_game_object_by_name('skip')
        ani.set_player(player)
        def sk():
            self.is_running = False
        skip.on_click.add_lisner(sk)
        #end
        self.scene.brightening_scene()
        stroy.update()
        while self.is_running:
            GameTime.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            
                    

            manger.layers.update()
            manger.layers.render()
            pygame.display.update()
        stroy.quit()
        self.is_running = True
        self.checkpoint = 'lab'

    def laboratory(self):
        self.scene.darkening_scene()
        manger.Layers.load('src/level/laboratory.json')
        manger.layers.mod = 'play'
        # awake
        button = manger.layers.get_game_object_by_name("enter")
        player = manger.layers.get_game_object_by_name('super')
        ani = manger.layers.get_game_object_by_name("chatbox")
        ani.set_player(player)
        button.on_click.add_lisner(lambda : ani.say('src/chat/test.json', 5))
        core = manger.layers.get_game_object_by_name("core")
        core.set_world(self)
        #end
        self.scene.brightening_scene()

        while self.is_running:
            GameTime.tick(60)
            
            for event in pygame.event.get():
                player.player_event(event)
                if event.type == pygame.QUIT:
                    quit()

            manger.layers.update()
            manger.layers.render()
            pygame.display.update()
            
        if self.game_over:
            raise Exception("GameOver")
        
        self.checkpoint = 'mountain'
            
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
    end = False
    game = AiDefenseGame(size=(1000, 800))
    while not end:
        try:
            if game.checkpoint == None:
                game.start()
                game.prologue()
            elif game.checkpoint == 'lab':
                game.laboratory()
            #game.mountain()
            #game.last_laboratory()
            else:
                end = True
                print("hel32le")
        except Exception:
            game.over()
    print("helle")
    pygame.quit() # 종료
    sys.exit()