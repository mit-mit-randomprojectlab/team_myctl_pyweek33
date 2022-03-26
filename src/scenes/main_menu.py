import pygame
from src.scenes.gamescene import GameScene
from src.gamedirector import GameDirector
from src.utils import make_text
import src.constants as constants

import os

from src.resource_manager import ResourceManager

class MainMenu(GameScene):
    def __init__(self, director: GameDirector, window_size):
        super().__init__(director)
        self.window_size = window_size

    # method gets called when director makes this the active scene
    def on_switchto(self, switchtoargs):
        pygame.mixer.music.stop()
        path = os.path.join(constants.RESOURCES_PATH, "music", "game_background.ogg")
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)

    # used to update physics, in-game states
    def on_update(self):
        pass

    # note/respond to incoming control inputs
    def on_event(self, events):
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.button1.collidepoint(mx, my):
                        #self.director.change_scene("maingame", [constants.LEVELS[0]])
                        pygame.mixer.music.stop()
                        self.director.change_scene("introscene", ['intro'])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.director.change_scene(None, [])

    def draw_game(self, screen):

        # fill background (write over previously drawn data from past frames)
        screen.fill(constants.COLOR.BLACK.value)
        
        screen.blit(ResourceManager().get_image("mainmenu.png"), (0,0))
        
        """
        self.title = make_text(
            "Game Title", constants.TITLE_FONT, constants.COLOR.WHITE.value, 150, 100
        )
        screen.blit(*self.title)
        """
        self.button1 = pygame.Rect(320, 230, 160, 50)
        pygame.draw.rect(screen, (0,150,0), self.button1)
        self.button1_text = make_text(
            "New Game", constants.MENU_ITEM_FONT, constants.COLOR.WHITE.value, 330, 240
        )
        screen.blit(*self.button1_text)

    # render the whole scene to the screen each frame
    def on_draw(self, screen):
        self.draw_game(screen)
