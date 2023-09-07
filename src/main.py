import pygame
import manger
import sys

from gametime import GameTime
from camera import camera
from story import Story
from scene import Scene

def story(story_path):
    def real_story(func):
        def wrapper(self):
            manger.layers.mod = 'story'
            self.story = story_path
            story = Story(story_path, self)
            story.update()
            func(self)
            story.quit()
        return wrapper
    return real_story

def world(world_path, checkpoint=None):
    def real_world(func):
        def wrapper(self):
            self.checkpoint = checkpoint
            manger.scene.darkening_scene()
            manger.layers.load(world_path)
            func(self)
            manger.layers.clear()
        return wrapper
    return real_world


class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        self.game_over = False
        manger.game = self
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        manger.screen = pygame.display.set_mode(size)
        manger.scene = Scene()
        self.width,self.height  = size
        self.is_running = True
        self.checkpoint = None
    
    def game_loop(self, *event_func):
        while self.is_running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                for func in event_func:
                    func(event)
            if manger.thread_connect.plz_wait:
                with manger.thread_connect.condition:
                    manger.thread_connect.condition.wait(3)
            manger.layers.update()
            manger.layers.render()
            pygame.display.flip()


    def start(self):
        
        manger.layers.load('D:/AI_DefenseGame/src/level/main.json')
        
        def wait(event): 
            if event.type == pygame.KEYDOWN:
                self.is_running = False
        self.game_loop(
            wait
        )
    
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

    def end(self):
        manger.screen.fill((0, 0, 0))
        manger.layers.clear()
        manger.Text("end", (500, 400), 50, "끝!", (255, 255, 255))
        manger.layers.render()
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    @world('D:/AI_DefenseGame/src/level/prologue.json', 'lab')
    @story('D:/AI_DefenseGame/src/story/prologue.json')
    def prologue(self):
        player = manger.layers.get_game_object_by_name('player')
        ani = manger.layers.get_game_object_by_name("playerChat")
        skip : manger.Button = manger.layers.get_game_object_by_name('skip')
        ani.set_player(player)
        def sk():
            self.is_running = False
        skip.on_click.add_lisner(sk)
        #end
        manger.scene.brightening_scene()

        self.game_loop()


    @world('D:/AI_DefenseGame/src/level/laboratory.json', 'mountain')
    def laboratory(self):
        # awake
        button = manger.layers.get_game_object_by_name("enter")
        player = manger.layers.get_game_object_by_name('super')
        ani = manger.layers.get_game_object_by_name("chatbox")
        ani.set_player(player)
        button.on_click.add_lisner(lambda : ani.say('D:/AI_DefenseGame/src/chat/test.json', 5))

        #end
        manger.scene.brightening_scene()

        self.game_loop(
            player.player_event
        )
        
        if self.game_over:
            raise Exception("GameOver")
        
    @world('D:/AI_DefenseGame/src/level/mountain.json', 'last_laboratory')
    def mountain(self):
        # awake
        
        #end
        manger.scene.brightening_scene()
        
        self.game_loop()
            
        if self.game_over:
            raise Exception("GameOver")
        
    @world('D:/AI_DefenseGame/src/level/last_laboratory.json', 'last_laboratory')
    def last_laboratory(self):
        # awake
        
        #end
        manger.scene.brightening_scene()
        
        self.game_loop()
        
        if self.game_over:
            raise Exception("GameOver")
                
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
            #elif game.checkpoint == 'mountain':
            #    game.mountain()
            #elif game.checkpoint == 'last_laboratory':
            #    game.last_laboratory()
            else:
                end = True
        except Exception:
            game.over()
    game.end()
    pygame.quit() # 종료
    sys.exit()
