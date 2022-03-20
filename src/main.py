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


# Start
def main(mainpath):

    # Initialise pygame
    pygame.init()
    pygame.mixer.init()
    import src.constants as constants
    import resources
    import scenes.game as game
    import scenes.main_menu as menu

    # pygame.mouse.set_visible(False) # might turn off if want mouse gone

    # start up director
    framerate = constants.FRAME_RATE  # suggested 30fps, can modify if needed
    window_size = (
        constants.WINDOW_SIZE_X,
        constants.WINDOW_SIZE_Y,
    )  # arbitrarily set for now
    window_title = constants.WINDOW_TITLE
    director = GameDirector(window_title, window_size, framerate)

    # Load all global resources (sprites, sounds, music etc.)
    resources.init(mainpath, window_size)

    # Load game scenes
    # For now, I've got a very basic "MainGame"
    mainmenu = menu.MainMenu(director, window_size)
    director.addscene("mainmenu", mainmenu)
    maingame = game.MainGame(director, window_size)
    director.addscene("maingame", maingame)

    # start up director
    director.change_scene("mainmenu", [])
    director.loop()
