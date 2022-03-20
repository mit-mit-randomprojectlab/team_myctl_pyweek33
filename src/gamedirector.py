#!/usr/bin/python

"""
gamedirector.py: classes for running the game using a director/scene structure
"""

import pygame
from pygame.locals import *

class GameDirector(object):
    def __init__(self, title, window_size, fps):
        
        # reference to pygame framebuffer
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        pygame.display.set_caption(title)
        
        self.fps = fps
        self.scene = None
        self.scenelist = {} # will contain a dictionary of loaded scenes
        
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        
        self.frame = 0
    
    def loop(self):
        
        while not self.quit_flag:
            self.time = self.clock.tick(self.fps)
            self.frame = self.frame + 1
            
            # Check for exit events
            # doing a bit of quick filtering to detect if players close window using mouse
            filtered_events = []
            for event in pygame.event.get():
                quitevent = False
                if event.type == pygame.QUIT:
                    self.quit()
                    quitevent = True
                if not quitevent:
                    filtered_events.append(event)
            
            # Run event handling for loaded scene
            self.scene.on_event(filtered_events)
            
            # Update scene
            self.scene.on_update()
            
            # Draw the screen
            self.scene.on_draw(self.screen)
            pygame.display.flip()
    
    # addscene: used during game initialisation
    def addscene(self, scenename, sceneobj):
        self.scenelist[scenename] = sceneobj
    
    # change_scene: tell director ro switch to new scene
    def change_scene(self, scenename, switchtoargs):
        if scenename is None: # switching to a "None" scene exits game
            self.quit()
        else:
            self.scene = self.scenelist[scenename]
            self.scene.on_switchto(switchtoargs) # run scene-specific method when switching-in
        
    def quit(self):
        self.quit_flag = True

# GameScene: Prototype for Scenes
class GameScene(object):
    def __init__(self, director):
        self.director = director
    
    # method gets called when director makes this the active scene
    def on_switchto(self, switchtoargs):
        raise NotImplementedError("on_switchto abstract method must be defined in subclass")
    
    # used to update physics, in-game states
    def on_update(self):
        raise NotImplementedError("on_update abstract method must be defined in subclass")
    
    # note/respond to incoming control inputs
    def on_event(self, event):
        raise NotImplementedError("on_event abstract method must be defined in subclass")
    
    # render the whole scene to the screen each frame
    def on_draw(self, screen):
        raise NotImplementedError("on_draw abstract method must be defined in subclass")

