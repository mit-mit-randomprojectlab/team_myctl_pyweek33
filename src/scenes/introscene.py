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
scene_data = []

# image: <gfx_tag> <snd_tag>
scene_data.append(['image','intro001','test001'])
scene_data.append(['image','intro001','test002'])
scene_data.append(['image','intro002','test001'])
scene_data.append(['image','intro002','test002'])

# conv: <left_gfx_tag> <right_gfx_tag> <snd_tag>
scene_data.append(['conv',None,None,'test001','scientist'])
scene_data.append(['conv',None,'evilface_happy','test001','evil'])
scene_data.append(['conv','goodface_happy','evilface_happy','test002','good'])
scene_data.append(['conv','goodface_happy','evilface_evil','test001','evil'])
scene_data.append(['conv','goodface_concern','evilface_evil','test002','good'])

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
        
        # reserve channel 0 here for voice in cutscene
        self.voice_channel = pygame.mixer.Channel(0)
        
        # animation variables
        self.ani_to = 0
        self.ani_frame = 0
        
        self.index = -1
        self.next = True
    
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

    def on_update(self):
        
        # pass new data
        if self.next == True:
            self.index += 1
            if self.index >= len(scene_data):
                self.director.change_scene("maingame", [])
                return
            data = scene_data[self.index]
            if data[0] == 'image':
                snd_tag = data[2]
                self.PlayVoice(snd_tag)
            elif data[0] == 'conv':
                snd_tag = data[3]
                self.PlayVoice(snd_tag)
            self.next = False
        elif not self.CheckVoice():
            self.next = True
        
        # Update animations
        self.ani_to += 1
        if self.ani_to > 3:
            self.ani_to = 0
            self.ani_frame = (self.ani_frame+1) % 2

    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.change_scene("maingame", [])
            elif event.type == KEYDOWN:
                self.next = True # trigger to next step
                self.StopVoice()
                
    def on_draw(self, screen):
        screen.fill(constants.COLOR.BLACK.value)
        
        data = scene_data[self.index]
        if data[0] == 'image':
            gfx_tag_stub = data[1]
            gfx_tag = gfx_tag_stub+['_a','_b'][self.ani_frame] # for which ani frame
            screen.blit(self.resource_gfx[gfx_tag], (0, 0))
        elif data[0] == 'conv':
            
            screen.fill((100,100,100))
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
            
        pygame.display.update()
        
