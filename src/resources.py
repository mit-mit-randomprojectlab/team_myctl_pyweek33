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
    ]
    for sprite in sprites:
        ResourceManager().get_image(sprite)

    # Load sound data
    # TODO

    # Load music data
    # TODO

    # etc ....
