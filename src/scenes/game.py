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
from src.models import Crystal
from src.models import Spritesheet
from src.models import TileMap

from src.resource_manager import ResourceManager

# MainGame: scene to run the main in-game content
class MainGame(GameScene):
    def __init__(self, director, window_size):
        super(MainGame, self).__init__(director)
        self.window_size = window_size

        # Background
        self.good_surf = pygame.Surface((400, 600))
        self.evil_surf = pygame.Surface((400, 600))
        
        # Test
        self.temp_surf = pygame.Surface(window_size).convert_alpha()
        self.bg_surf = pygame.Surface(window_size)
        self.bg_surf.fill((0,0,0))
        self.bg_surf.convert()
        self.bg_surf.set_alpha(128)
        
        self.music = None
        
        # Use this space to initialise anything that only needs to be done when the game/app
        # first starts up and not again

    def on_switchto(self, switchtoargs):

        # Use this space to initialise things that need to be done every time the game switches
        # back to this scene (i.e. could happen multiple time in a game).
        # I recommend re-instantiating in-game objects here (e.g. like the player, and put
        # the player starting data in it's __init__() method etc. ...
        
        if switchtoargs[0] == None:
            return # returning from pausescene, leave game as is
        
        # the level we will load
        self.level = switchtoargs[0]
        ind = constants.LEVELS.index(self.level)
        if ind == 0:
            self.music = None
        
        # Setup Music
        if self.music == None:
            pygame.mixer.music.stop()
            if ind == len(constants.LEVELS)-1:
                path = os.path.join(constants.RESOURCES_PATH, "music", "scientists_remix.ogg")
                self.music = 'loopfinal'
            else:
                path = os.path.join(constants.RESOURCES_PATH, "music", "game_background.ogg")
                self.music = 'loop'
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
        
        # load the sprite sheet for tilemap
        sheetpath = os.path.join(constants.RESOURCES_PATH,'spritesheet','spritesheet.png')
        self.spritesheet = Spritesheet(sheetpath)
        
        # Good world tilemap
        good_lvl_path = os.path.join(constants.RESOURCES_PATH,'levels','good_%s.csv'%(self.level))
        self.tilemap_good = TileMap(good_lvl_path,self.spritesheet)
        
        # Evil world tilemap
        evil_lvl_path = os.path.join(constants.RESOURCES_PATH,'levels','evil_%s.csv'%(self.level))
        self.tilemap_evil = TileMap(evil_lvl_path,self.spritesheet)
        
        # Player (moved here to help with scene transitions later)
        self.good = pygame.sprite.GroupSingle()
        self.good.add(Player(self,"good", 32*3, 32*3))
        self.evil = pygame.sprite.GroupSingle()
        self.evil.add(Player(self,"evil", 32*3+400, 32*3))
        
        # Occupancy grid (moved here to help with scene transitions later)
        self.occmanager = OccupancyManager(12,18,good_lvl_path,evil_lvl_path,offset_good=(8,12),offset_evil=(408,12))
        
        # UI Stuff (pre-rendered text surfaces)
        self.fail_text = make_text(
            "Level Failed!", constants.BIG_FONT, (250,0,0), 200, 10
        )
        self.fail_text[1][0] = 400-self.fail_text[1][2]/2 # center in x
        self.fail_text_bg = pygame.Surface((self.fail_text[1][2], self.fail_text[1][3])).convert_alpha()
        self.fail_text_bg.fill((0,0,0))
        self.fail_text_bg.set_alpha(100)
        
        self.complete_text = make_text(
            "Level Complete!", constants.BIG_FONT, (0,100,250), 200, 10
        )
        self.complete_text[1][0] = 400-self.complete_text[1][2]/2 # center in x
        self.complete_text_bg = pygame.Surface((self.complete_text[1][2], self.complete_text[1][3])).convert_alpha()
        self.complete_text_bg.fill((0,0,0))
        self.complete_text_bg.set_alpha(128)
        
        # Green Crystal (goal) location
        self.crystal = Crystal(self.tilemap_good.crystal_loc, self.good, self.spritesheet.sprite_sheet)
        
        # Game variables
        self.reach_goal = False # triggered if get green crystal (TODO)
        self.touch_evil = False # triggered by player if evil touches objects
        self.touch_evil_loc = (0,0)
        self.level_complete = False
        self.level_fail = False
        self.reset_countdown = 90

    def on_update(self):
        self.tilemap_good.UpdateAnimations()
        self.tilemap_evil.UpdateAnimations()
        
        self.crystal.Update()
        if self.crystal.pickedup == True:
            self.reach_goal = True
            if self.reset_countdown == 90:
                # for example play sound for complete level
                ResourceManager().get_sound("good_win.ogg","sound").play()
                ResourceManager().get_sound("gem.ogg", "sound").play()
        
        # check for end level transitions
        if self.reach_goal:
            self.level_complete = True
        elif self.touch_evil:
            self.level_fail = True
            if self.reset_countdown == 90:
                # for example play sound for failed level
                ResourceManager().get_sound("evilfailure.ogg","sound").play()
                ResourceManager().get_sound("failed.ogg","sound").play()
        if self.reach_goal or self.level_fail:
            self.reset_countdown -= 1
            if self.reset_countdown <= 0:
                if self.level_complete:
                    ind = constants.LEVELS.index(self.level)
                    if ind < len(constants.LEVELS)-2: # go to next level
                        self.director.change_scene("maingame", [constants.LEVELS[ind+1]])
                    elif ind < len(constants.LEVELS)-1:
                        self.music = None
                        pygame.mixer.music.stop()
                        self.director.change_scene("introscene", ['finallevel'])
                    else:
                        self.music = None
                        pygame.mixer.music.stop()
                        self.director.change_scene("introscene", ['victory'])
                elif self.level_fail:
                    self.director.change_scene("maingame", [self.level])

        # I suggest all in game objects that need updating should have their own update()
        # method, and these are all called here
            

    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                #self.director.change_scene("mainmenu", [])
                self.draw_game(self.temp_surf)
                self.temp_surf.blit(self.bg_surf, (0, 0))
                self.director.change_scene("pausescene", [self.level, self.temp_surf])
                # this is the basic way we might be able to switch from one scene to another:
                # each scene has a reference to the director, and then when they are ready to
                # transfer to the next scene, they just call director.change_scene() ...
            elif event.type == KEYDOWN or event.type == KEYUP:
                pass  # TODO: pass to another object to handle?

    def draw_game(self, screen):

        screen.fill(constants.COLOR.BLACK.value)
        
        # background for each world
        self.good_surf.fill((0, 0, 100))
        self.evil_surf.fill((100, 0, 0))
        screen.blit(self.good_surf, (0, 0))
        screen.blit(self.evil_surf, (400, 0))
        
        # Draw tilemap
        screen.blit(self.tilemap_good.map_surface, (8,12))
        screen.blit(self.tilemap_evil.map_surface, (408,12))
        
        # draw occupancy grid
        #self.occmanager.DrawTest(screen)
        
        # draw flashing tile on level fail
        if self.level_fail and self.reset_countdown % 10 < 5:
            pygame.draw.rect(screen,(255,255,255),(self.touch_evil_loc[0],self.touch_evil_loc[1],32,32))
        
        # Draw Green Crystal
        self.crystal.Draw(screen)
        
        # Draw player
        self.good.draw(screen)
        self.good.update()
        self.evil.draw(screen)
        self.evil.update()
        
        # UI Stuff
        if self.level_fail:
            screen.blit(self.fail_text_bg, (self.fail_text[1][0]-8,self.fail_text[1][1]))
            screen.blit(*self.fail_text)
        elif self.level_complete:
            screen.blit(self.complete_text_bg, (self.complete_text[1][0]-8,self.complete_text[1][1]))
            screen.blit(*self.complete_text)

        # TODO: I recommend all objects that need to be drawn have their own draw() method
        # and these all get called here

    def on_draw(self, screen):
        self.draw_game(screen)
        pygame.display.update()
        # splitting out into two functions here (i.e. "on_draw" and "draw_game") makes it easier
        # in the future to do things like render fade in/outs, pause screens, other effects ect.
        # on top of the regular drawing of objects (specified in "draw_game")
