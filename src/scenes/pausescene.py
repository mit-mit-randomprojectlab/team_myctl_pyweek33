#!/usr/bin/python

"""
pausescene.py: scene class to handle pause menu
"""

import os
import pygame
from pygame.locals import *
from gamedirector import *

from src.scenes import GameScene
from src.utils import make_text
import src.constants as constants

import src.resources

# MainGame: scene to run the main in-game content
class PauseScene(GameScene):
    def __init__(self, director, window_size):
        super(PauseScene, self).__init__(director)
        self.window_size = window_size

        # UI Stuff (pre-rendered text surfaces)
        self.pause_text = make_text(
            "Paused", constants.BIG_FONT, (250,250,250), 0, 200
        )
        self.pause_text[1][0] = 400-self.pause_text[1][2]/2 # center in x
        
        self.return_text = make_text(
            "ESC: Return to Game", constants.BIG_FONT, (0,250,0), 0, 300
        )
        self.return_text[1][0] = 400-self.return_text[1][2]/2 # center in x
        
        self.reset_text = make_text(
            "R: Reset Level", constants.BIG_FONT, (0,250,0), 0, 350
        )
        self.reset_text[1][0] = 400-self.reset_text[1][2]/2 # center in x
        
        self.quit_text = make_text(
            "Q: Quit to Menu", constants.BIG_FONT, (0,250,0), 0, 400
        )
        self.quit_text[1][0] = 400-self.quit_text[1][2]/2 # center in x

    def on_switchto(self, switchtoargs):
        self.level_from = switchtoargs[0]
        self.bg_surf = switchtoargs[1]
        
    def on_update(self):
        pass

    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.change_scene("maingame", [None])
            elif event.type == KEYDOWN and event.key == K_r: # reset level
                self.director.change_scene("maingame", [self.level_from])
            elif event.type == KEYDOWN and event.key == K_q: # quit to menu
                pygame.mixer.music.stop()
                self.director.change_scene("mainmenu", [None])
                
    def on_draw(self, screen):
        screen.fill(constants.COLOR.BLACK.value)
        screen.blit(self.bg_surf, (0, 0))
        screen.blit(*self.pause_text)
        screen.blit(*self.return_text)
        screen.blit(*self.reset_text)
        screen.blit(*self.quit_text)
        pygame.display.update()

        