#!/usr/bin/python

"""
introscene.py: intro cutscene scene classes
"""

import os
import pygame
from pygame.locals import *
from gamedirector import *

from src.scenes import GameScene
from src.utils import make_text
import src.constants as constants

import src.resources

# For now just storing scene sequence here
scene_data_intro = []

# Intro Scene:

# image: <gfx_tag> <snd_tag>
scene_data_intro.append(['image','intro001','introsci001'])
scene_data_intro.append(['image','intro002','introsci002'])
scene_data_intro.append(['image','intro003','introsci003'])
scene_data_intro.append(['image','intro004','introsci004'])
scene_data_intro.append(['image','intro004','introsci005'])
scene_data_intro.append(['image','intro005','introsci006'])
scene_data_intro.append(['image','intro006','intro_machine'])
scene_data_intro.append(['image','intro007','scream'])

# conv: <left_gfx_tag> <right_gfx_tag> <snd_tag>
scene_data_intro.append(['conv','goodface_happy','evilface_happy','scientist001','scientist','loop001a'])

scene_data_intro.append(['conv','goodface_happy','evilface_happy','evil001','evil'])

scene_data_intro.append(['conv','goodface_happy','evilface_happy','scientist002','scientist'])

scene_data_intro.append(['conv','goodface_happy2','evilface_suprise','good001','good'])

scene_data_intro.append(['conv','goodface_happy','evilface_happy','scientist003','scientist'])

scene_data_intro.append(['conv','goodface_happy','evilface_suprise','good002','good'])
scene_data_intro.append(['conv','goodface_happy','evilface_suprise','good002a','good','loop001a','crystal'])

scene_data_intro.append(['conv','goodface_concern','evilface_evil','evil002a','evil'])
scene_data_intro.append(['conv','goodface_concern','evilface_evil','evil002b','evil','loop001a','evil'])

scene_data_intro.append(['conv','goodface_concern','evilface_evil','good003','good'])

scene_data_intro.append(['conv','goodface_concern','evilface_suprise','evil003a','evil'])
scene_data_intro.append(['conv','goodface_concern','evilface_evil','evil003b','evil'])

scene_data_intro.append(['conv','goodface_concern','evilface_evil','good004','good'])

# Final Level Scene:
scene_data_finallevel = []

scene_data_finallevel.append(['conv','goodface_happy','evilface_suprise','finallevel','good'])
scene_data_finallevel.append(['conv','goodface_happy2','evilface_evil','evil003a','evil'])

# End Game/Victory Scene:
scene_data_victory = []

scene_data_victory.append(['image','final001','machine_shutdown'])
scene_data_victory.append(['image','final001a','machine_shutdown'])
scene_data_victory.append(['image','final002','noise'])
scene_data_victory.append(['image','final003','noise'])
scene_data_victory.append(['image','final004','noise'])
scene_data_victory.append(['image','final005','noise'])
scene_data_victory.append(['image','final006','finalspeech'])
scene_data_victory.append(['image','final_outside','playout'])

# MainGame: scene to run the main in-game content
class IntroCutScene(GameScene):
    def __init__(self, director, window_size):
        super(IntroCutScene, self).__init__(director)
        self.window_size = window_size

        # Load resources locally (for now)
        folderpath = os.path.join(constants.RESOURCES_PATH,'cutscene')
        
        self.resource_gfx = {}
        file_paths = [i for i in os.listdir(folderpath) if "png" in i]
        for f in file_paths:
            self.resource_gfx[f[:-4]] = pygame.image.load(os.path.join(folderpath,f)).convert_alpha()
        
        self.resource_snd = {}
        file_paths = [i for i in os.listdir(folderpath) if "ogg" in i]
        for f in file_paths:
            self.resource_snd[f[:-4]] = pygame.mixer.Sound(os.path.join(folderpath,f))
        
        # setup background circles
        self.bg_circle_good = pygame.Surface(window_size)
        self.bg_circle_good.fill((0,0,0))
        self.bg_circle_good.convert()
        self.bg_circle_good.set_colorkey((0,0,0))
        pygame.draw.circle(self.bg_circle_good, (0,0,100), (150,450), 250)
        self.bg_circle_good.set_alpha(128)
        
        self.bg_circle_evil = pygame.Surface(window_size)
        self.bg_circle_evil.fill((0,0,0))
        self.bg_circle_evil.convert()
        self.bg_circle_evil.set_colorkey((0,0,0))
        pygame.draw.circle(self.bg_circle_evil, (100,0,0), (650,450), 250)
        self.bg_circle_evil.set_alpha(128)

    def on_switchto(self, switchtoargs):
        
        self.scenetag = switchtoargs[0]
        if self.scenetag == 'intro':
            self.scene_data = scene_data_intro
        elif self.scenetag == 'finallevel':
            self.scene_data = scene_data_finallevel
        elif self.scenetag == 'victory':
            self.scene_data = scene_data_victory
        
        # reserve channel 0 here for voice in cutscene
        self.voice_channel = pygame.mixer.Channel(0)
        
        # animation variables
        self.ani_to = 0
        self.ani_frame = 0
        
        self.index = -1
        self.next = True
        self.extragfx = None
        self.fadeto = 0
        
        self.currentmusic = None
    
    def PlayVoice(self, tag):
        self.voice_channel.play(self.resource_snd[tag])
    
    def PauseVoice(self):
        self.voice_channel.pause()
    
    def ResumeVoice(self):
        self.voice_channel.unpause()
    
    def StopVoice(self):
        self.voice_channel.stop()
    
    def CheckVoice(self):
        return self.voice_channel.get_busy()
    
    def SwitchMusic(self, tag):
        if not self.currentmusic == tag:
            pygame.mixer.music.stop()
            path = os.path.join(constants.RESOURCES_PATH,'music','%s.ogg'%(tag))
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            self.currentmusic = tag
        
    def ExtraGraphics(self, tag):
        self.fadeto = 30
        self.extragfx = tag
    
    def ResetExtraGraphics(self):
        self.extragfx = None
    
    def exiting(self):
        if self.scenetag == 'intro':
            self.director.change_scene("maingame", [constants.LEVELS[0]])
        if self.scenetag == 'finallevel':
            self.director.change_scene("maingame", [constants.LEVELS[-1]])
        elif self.scenetag == 'victory':
            self.director.change_scene("mainmenu", [])
    
    def on_update(self):
        
        # pass new data
        if self.next == True:
            self.index += 1
            if self.index >= len(self.scene_data):
                self.StopVoice()
                pygame.mixer.music.stop()
                self.exiting()
                return
            data = self.scene_data[self.index]
            if data[0] == 'image':
                snd_tag = data[2]
                self.PlayVoice(snd_tag)
            elif data[0] == 'conv':
                snd_tag = data[3]
                self.PlayVoice(snd_tag)
            self.next = False
            if len(data) == 6:
                self.SwitchMusic(data[5])
            if len(data) == 7:
                self.ExtraGraphics(data[6])
            else:
                self.ResetExtraGraphics()
        elif not self.CheckVoice():
            self.next = True
        
        # Update animations
        self.ani_to += 1
        if self.scene_data[self.index][1] == 'intro007':
            delay = 10
        else:
            delay = 3
        if self.ani_to > delay:
            self.ani_to = 0
            self.ani_frame = (self.ani_frame+1) % 2
        if self.fadeto > 0:
            self.fadeto -= 1

    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.StopVoice()
                pygame.mixer.music.stop()
                self.exiting()
            elif event.type == KEYDOWN:
                self.next = True # trigger to next step
                self.StopVoice()
                
    def on_draw(self, screen):
        screen.fill(constants.COLOR.BLACK.value)
        
        data = self.scene_data[self.index]
        if data[0] == 'image':
            gfx_tag_stub = data[1]
            gfx_tag = gfx_tag_stub+['_a','_b'][self.ani_frame] # for which ani frame
            screen.blit(self.resource_gfx[gfx_tag], (0, 0))
        elif data[0] == 'conv':
            
            screen.fill((100,100,100))
            screen.blit(self.resource_gfx['level_space'], (0, 0))
            screen.blit(self.resource_gfx['sil'], (250, 0))
            
            who_speak = data[4]
            if who_speak == 'good':
                screen.blit(self.bg_circle_good, (0,0))
            elif who_speak == 'evil':
                screen.blit(self.bg_circle_evil, (0,0))
            
            gfxleft_tag_stub = data[1]
            if not gfxleft_tag_stub == None:
                gfxleft_tag = gfxleft_tag_stub+['_a','_b'][self.ani_frame] # for which ani frame
                if who_speak == 'good':
                    self.resource_gfx[gfxleft_tag].set_alpha(255)
                else:
                    self.resource_gfx[gfxleft_tag].set_alpha(128)
                screen.blit(self.resource_gfx[gfxleft_tag], (0, 300))
            
            gfxright_tag_stub = data[2]
            if not gfxright_tag_stub == None:
                gfxright_tag = gfxright_tag_stub+['_a','_b'][self.ani_frame] # for which ani frame
                if who_speak == 'evil':
                    self.resource_gfx[gfxright_tag].set_alpha(255)
                else:
                    self.resource_gfx[gfxright_tag].set_alpha(128)
                screen.blit(self.resource_gfx[gfxright_tag], (500, 300))
            
            if self.extragfx == 'crystal':
                self.resource_gfx['crystal_big'].set_alpha(int(255*(30-self.fadeto)/30))
                screen.blit(self.resource_gfx['crystal_big'], (300, 300))
            elif self.extragfx == 'evil':
                self.resource_gfx['evil_objects'].set_alpha(int(255*(30-self.fadeto)/30))
                screen.blit(self.resource_gfx['evil_objects'], (420, 230))
            
        pygame.display.update()
        
