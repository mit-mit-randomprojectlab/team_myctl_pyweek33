import pygame

from src.resource_manager import ResourceManager


class Player(pygame.sprite.Sprite):
    def __init__(self, size: tuple = (50, 50)):
        super().__init__()
        self.image = pygame.transform.scale(
            ResourceManager().get_image("absol.png"), size
        )
        # self.rect = self.image.get_rect(midbottom=(200, 300))

    def draw(self, screen: pygame.surface.Surface, x: int, y: int):
        screen.blit(self.image, (x, y))
