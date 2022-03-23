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
from src.models import Wall

# TODO: put classes for in-game objects in other source files and import them
from src.models import Player
from src.models import OccupancyManager

# MainGame: scene to run the main in-game content
class MainGame(GameScene):
    def __init__(self, director, window_size):
        super(MainGame, self).__init__(director)
        self.window_size = window_size

        # Background
        self.good_surf = pygame.Surface((400, 600))
        self.evil_surf = pygame.Surface((400, 600))

        # Obstacles (no longer used: using occupancy grid now)
        #self.obstacles = pygame.sprite.Group()
        #self.obstacles.add(Wall(600, 300))

        # Player
        # mit-mit: added reference of this GameScene to player so they can access the
        # occmanager: not sure if this is the best practise :)?
        self.good = pygame.sprite.GroupSingle()
        self.good.add(Player(self,"good", 200, 300))
        self.evil = pygame.sprite.GroupSingle()
        self.evil.add(Player(self,"evil", 600, 300))
        
        # Occupancy grid
        self.occmanager = OccupancyManager(12,18,offset_good=(8,12),offset_evil=(408,12))
        # Use this space to initialise anything that only needs to be done when the game/app
        # first starts up and not again

    def on_switchto(self, switchtoargs):

        # Use this space to initialise things that need to be done every time the game switches
        # back to this scene (i.e. could happen multiple time in a game).
        # I recommend re-instantiating in-game objects here (e.g. like the player, and put
        # the player starting data in it's __init__() method etc. ...
        pass

    def on_update(self):
        pass

        # I suggest all in game objects that need updating should have their own update()
        # method, and these are all called here

    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.change_scene("mainmenu", [])
                # this is the basic way we might be able to switch from one scene to another:
                # each scene has a reference to the director, and then when they are ready to
                # transfer to the next scene, they just call director.change_scene() ...
            elif event.type == KEYDOWN or event.type == KEYUP:
                pass  # TODO: pass to another object to handle?

    def draw_game(self, screen):

        # fill background (write over previously drawn data from past frames)
        screen.fill(constants.COLOR.BLACK.value)
        self.good_surf.fill((208, 247, 247))
        self.evil_surf.fill((228, 184, 255))

        screen.blit(self.good_surf, (0, 0))
        screen.blit(self.evil_surf, (400, 0))
        self.occmanager.DrawTest(screen)

        self.good.draw(screen)
        self.good.update()
        self.evil.draw(screen)
        self.evil.update()
        #self.obstacles.draw(screen)
        #self.obstacles.update()

        # TODO: I recommend all objects that need to be drawn have their own draw() method
        # and these all get called here

    def on_draw(self, screen):
        self.draw_game(screen)
        pygame.display.update()
        # splitting out into two functions here (i.e. "on_draw" and "draw_game") makes it easier
        # in the future to do things like render fade in/outs, pause screens, other effects ect.
        # on top of the regular drawing of objects (specified in "draw_game")
