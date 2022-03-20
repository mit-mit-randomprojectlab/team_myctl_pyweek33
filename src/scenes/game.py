#!/usr/bin/python

"""
game.py: main in-game scene classes
"""

import os
import pygame
from pygame.locals import *
from gamedirector import *
from src.scenes import GameScene
from src.utils import make_text
import src.constants as constants

import src.resources

# TODO: put classes for in-game objects in other source files and import them
from src.models import Player

# MainGame: scene to run the main in-game content
class MainGame(GameScene):
    def __init__(self, director, window_size):
        super(MainGame, self).__init__(director)
        self.window_size = window_size

        # Use this space to initialise anything that only needs to be done when the game/app
        # first starts up and not again

    def on_switchto(self, switchtoargs):

        # Use this space to initialise things that need to be done every time the game switches
        # back to this scene (i.e. could happen multiple time in a game).
        # I recommend re-instantiating in-game objects here (e.g. like the player, and put
        # the player starting data in it's __init__() method etc. ...
        self.player = Player((100, 100))

    def on_update(self):
        pass

        # I suggest all in game objects that need updating should have their own update()
        # method, and these are all called here

    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.change_scene(
                    None, []
                )  # quit game for now, probably change later
                # this is the basic way we might be able to switch from one scene to another:
                # each scene has a reference to the director, and then when they are ready to
                # transfer to the next scene, they just call director.change_scene() ...
            elif event.type == KEYDOWN or event.type == KEYUP:
                pass  # TODO: pass to another object to handle?

    def draw_game(self, screen):

        # fill background (write over previously drawn data from past frames)
        screen.fill((0, 0, 0))

        self.player.draw(screen, 100, 200)
        text = make_text(
            "Main Game Scene", constants.MENU_ITEM_FONT, (255, 255, 255), 50, 10
        )

        screen.blit(*text)

        # TODO: I recommend all objects that need to be drawn have their own draw() method
        # and these all get called here

    def on_draw(self, screen):
        self.draw_game(screen)
        # splitting out into two functions here (i.e. "on_draw" and "draw_game") makes it easier
        # in the future to do things like render fade in/outs, pause screens, other effects ect.
        # on top of the regular drawing of objects (specified in "draw_game")
