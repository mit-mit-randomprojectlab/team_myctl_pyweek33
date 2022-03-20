from pathlib import Path
import src

# Single place to define project constants

FRAME_RATE = 30

WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600
WINDOW_TITLE = "The Game"

RESOURCES_PATH = Path(src.__file__).parent.parent.absolute() / "data"
