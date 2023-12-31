
import sys
import pygame

pygame.init()
pygame.display.set_caption("AI Defense Game")

import manger
from gametime import GameTime
from enemy import living_enemy
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
            manger.scene.darkening_scene()
            manger.layers.load(world_path)
            func(self)
            self.checkpoint = checkpoint
            manger.sound_manger.all_stop()
            manger.layers.clear()
        return wrapper
    return real_world

def empty_func():
    pass

class GameOver(Exception):
    pass

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        self.game_over = False
        manger.game = self
        manger.screen = pygame.display.set_mode(size)
        manger.scene = Scene()
        self.width,self.height  = size
        self.is_running = True
        self.checkpoint = None
    
    def game_loop(self, event_func, game_loop=empty_func):
        self.is_running = True
        self.game_over = False
        while self.is_running:
            GameTime.tick(60)   
            game_loop()
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
        manger.layers.load('./level/main.json')
        def wait(event): 
            if event.type == pygame.KEYDOWN:
                self.is_running = False
        self.game_loop(
            [wait]
        )
    
    def over(self):
        manger.screen.fill((0, 0, 0))
        manger.layers.clear()
        manger.Text("over", (500, 400), 50, "Game Over", (255, 255, 255))
        manger.layers.render()
        pygame.display.flip()
        waiting = True
        manger.sound_manger['game_over'].play()
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

    @world('./level/prologue.json', 'lab')
    @story('./story/prologue.json')
    def prologue(self):
        player = manger.layers.get_game_object_by_name('player')
        ani = manger.layers.get_game_object_by_name("enemyChat")
        enemy = manger.layers.get_game_object_by_name("enemy")
        skip : manger.Button = manger.layers.get_game_object_by_name('skip')
        ani.set_player(enemy)
        def sk():
            self.is_running = False
        skip.on_click.add_lisner(sk)
        manger.scene.brightening_scene()
        self.game_loop([])

    @world('./level/laboratory.json', 'mountain')
    def laboratory(self):
        # awake

        manger.scene.brightening_scene()

        def check_enemy():
            if living_enemy.is_emty():
                self.is_running = False
                
        self.game_loop(
            [manger.player.player_event],
            check_enemy
        )
        
        if self.game_over:
            raise GameOver("GameOver")
        
    @world('./level/mountain.json', 'last_laboratory')
    def mountain(self):
        # awake
        manger.player.skill_w_ev = True
        manger.player.skill_e_ev = False
        #end
        manger.scene.brightening_scene()
        
        def check_enemy():
            if living_enemy.is_emty():
                self.is_running = False
        
        self.game_loop(
            [manger.player.player_event],
            check_enemy
        )
         
        if self.game_over:
            raise GameOver("GameOver")
        
    @world('./level/last_laboratory.json', 'end')
    def last_laboratory(self):
        # awake
        core = manger.layers.get_game_object_by_name("core")
        manger.player.skill_e_ev = True 
        manger.player.skill_w_ev = True 
        #end
        manger.scene.brightening_scene()
        
        self.game_loop(
            [manger.player.player_event,
            core.core_event]
        )
        
        if self.game_over:
            raise GameOver("GameOver")
                
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
            elif game.checkpoint == 'mountain':
                game.mountain()
            elif game.checkpoint == 'last_laboratory':
                game.last_laboratory()
            else:
                end = True
        except Exception:
            game.over()
    game.end()
    pygame.quit() # 종료
    sys.exit()
