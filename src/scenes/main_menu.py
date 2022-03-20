import pygame
from src.scenes.gamescene import GameScene
from src.gamedirector import GameDirector
from src.utils import make_text
import src.constants as constants


class MainMenu(GameScene):
    def __init__(self, director: GameDirector, window_size):
        super().__init__(director)
        self.window_size = window_size

    # method gets called when director makes this the active scene
    def on_switchto(self, switchtoargs):
        pass

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
                        self.director.change_scene("maingame", [])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.director.change_scene(None, [])

    def draw_game(self, screen):

        # fill background (write over previously drawn data from past frames)
        screen.fill((0, 0, 0))

        self.title = make_text(
            "Game Title", constants.TITLE_FONT, (255, 255, 255), 150, 100
        )
        screen.blit(*self.title)
        self.button1 = pygame.Rect(150, 200, 160, 50)
        pygame.draw.rect(screen, (255, 0, 0), self.button1)
        self.button1_text = make_text(
            "Main Game", constants.MENU_ITEM_FONT, (255, 255, 255), 170, 210
        )
        screen.blit(*self.button1_text)

    # render the whole scene to the screen each frame
    def on_draw(self, screen):
        self.draw_game(screen)
