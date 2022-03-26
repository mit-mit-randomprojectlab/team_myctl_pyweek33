from pathlib import Path
import pygame
import src
from enum import Enum
import os

# Single place to define project constants

FRAME_RATE = 30

WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600
WINDOW_TITLE = "The Game"

RESOURCES_PATH = Path(src.__file__).parent.parent.absolute() / "data"

# Fonts
TITLE_FONT = pygame.font.SysFont(None, 40)
MENU_ITEM_FONT = pygame.font.SysFont(None, 40)

#BIG_FONT = pygame.font.SysFont(None, 80)
BIG_FONT = pygame.font.Font(os.path.join(RESOURCES_PATH,'BabyMarker-1GZaL.ttf'), 40)

LEVELS = [
    "clutter",
    "channels",
    "singlebend",
    "thebox",
    "themaze",
    "thelock"
    ]

# Colors
class COLOR(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
