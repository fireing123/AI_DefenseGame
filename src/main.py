import pygame
# not import my module
import manger
from gametime import GameTime
from camera import Camera
#import module first
#None
#import module second
from ui import Button, ChatBox # event, object, sheet(color), animation(object)
#import module fourth
from scene import Scene
#camera, background(object)
#layer (
# object, background(object), ground(object)
# ui(event, object, sheet(color), animation(object))
# player(object, animation(object), sheet(color), ground(object))
#)

class AiDefenseGame:
    
    def __init__(self, size=(500, 500)):
        pygame.init()
        pygame.display.set_caption("AI Defense Game")
        self.width,self.height  = size
        self.screen = pygame.display.set_mode(size)
        manger.screen = self.screen
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
                    break
                if event.type == pygame.KEYUP:
                    waiting = False

    def main(self):
        
        self.scene.darkening_scene()
        new_scene = Scene.load('src/level/laboratory.json', self.screen)
        del self.scene
        self.scene = new_scene
        # awake
        layers = self.scene.layers
        button : Button = layers.get_game_object_by_name("enter")
        player = layers.get_game_object_by_name('super')
        ani : ChatBox = layers.get_game_object_by_name("chatbox")
        button.event.add_lisner(lambda : ani.say('src/chat/test.json', 5))
        ani.set_player(player)
        #end
        new_scene.brightening_scene()

        while self.is_running:
            GameTime.tick(60)
            for event in pygame.event.get():
                player.player_event(event)
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        cvx, cvy = Camera.vector
                        Camera.vector = cvx - 5, cvy
                    if event.key == pygame.K_d:
                        cvx, cvy = Camera.vector
                        Camera.vector = cvx + 5, cvy
            self.scene.update()
            self.scene.render()
            pygame.display.update()
            
        pygame.quit() # 종료
        
if __name__ == "__main__" :
    game = AiDefenseGame(size=(1000, 800))
    game.start()
    game.main()