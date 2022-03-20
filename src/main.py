#!/usr/bin/python

"""
main.py: Main entry point for game
- initialises pygame
- Starts up the game director
- loads and inits all scenes
- Starts main director game loop
"""

import os
import pygame
from pygame.locals import *
from gamedirector import *

import resources
import game

# Start
def main(mainpath):

    # Initialise pygame
    pygame.init()
    pygame.mixer.init()
    #pygame.mouse.set_visible(False) # might turn off if want mouse gone
    
    # start up director
    framerate = 30 # suggested 30fps, can modify if needed
    window_size = (800,600) # arbitrarily set for now
    window_title = "The Game"
    dir = GameDirector(window_title, window_size, framerate)
    
    # Load all global resources (sprites, sounds, music etc.)
    resources.init(mainpath, window_size)
    
    # Load game scenes
    # For now, I've got a very basic "MainGame"
    maingame = game.MainGame(dir, window_size)
    dir.addscene('maingame', maingame)
    
    # start up director
    dir.change_scene('maingame', [])
    dir.loop()
    
