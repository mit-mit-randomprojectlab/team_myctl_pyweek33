#!/usr/bin/python

"""
resources.py: Load all resource data once 
"""

import os, sys
import pygame
from pygame.locals import *

from src.resource_manager import ResourceManager
from src.models import Player


def init(mainpath, window_size):

    # Load sprites
    sprites = [
        "absol.png",
        "playergood_idle0.png",
        "playergood_idle1.png",
        "playergood_idle2.png",
        "playergood_walk0.png",
        "playergood_walk1.png",
        "playergood_walk2.png",
        "playergood_walk3.png",
        "playergoodback_walk0.png",
        "playergoodback_walk1.png",
        "playergoodback_walk2.png",
        "playergoodback_walk3.png",
        "tilemap001.png",
    ]
    for sprite in sprites:
        ResourceManager().get_image(sprite)

    # Load sound data
    sounds = [
        "good_win.ogg",
        "evilfailure.ogg",
    ]
    for sound in sounds:
        ResourceManager().get_sound(sound)

    # etc ....
