import pygame
import os
import csv

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x ,y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def draw_tile(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    
class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0
        for row in map:
            x = 0
            for tile in row:
                #here will be where each tile gets its respective png
                break



        