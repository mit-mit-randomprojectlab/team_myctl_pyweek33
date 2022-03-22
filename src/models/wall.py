import pygame
from src.resource_manager import ResourceManager


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.wall = ResourceManager().get_image("orange_rectangle.png")
        self.wall = pygame.transform.scale2x(self.wall)
        self.x = int(x)
        self.y = int(y)
        self.image = self.wall
        self.rect = self.image.get_rect(midbottom=(x, y))
