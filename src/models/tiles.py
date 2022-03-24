import pygame
import os
import csv

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x ,y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    
class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        #self.map_surface.set_colorkey(0, 0, 0)
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))
    

    def load_map(self):
        self.map_surface.fill((100,100,100))
        for tile in self.tiles:
            tile.draw(self.map_surface)

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
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == "0":
                    tiles.append(Tile("big_table_horizontal.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "1":
                    tiles.append(Tile("big_table_horizontal2.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "2":
                    tiles.append(Tile("big_table_vertical.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "3":
                    tiles.append(Tile("big_table_vertical2.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "4":
                    tiles.append(Tile("cactus_table.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "5":
                    tiles.append(Tile("computer_table.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "6":
                    tiles.append(Tile("computer_table2.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "7":
                    tiles.append(Tile("door.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "8":
                    tiles.append(Tile("evil_barrier.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "9":
                    tiles.append(Tile("evil_barrier2.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "16":
                    tiles.append(Tile("evil_bumper.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "17":
                    tiles.append(Tile("evil_door.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "18":
                    tiles.append(Tile("evil_elec1.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "21":
                    tiles.append(Tile("evil_toxic.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "22":
                    tiles.append(Tile("graph_wall.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "23":
                    tiles.append(Tile("misc_horizontal.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "24":
                    tiles.append(Tile("misc_horizontal2.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "25":
                    tiles.append(Tile("misc_wall.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "26":
                    tiles.append(Tile("plain_wall.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "27":
                    tiles.append(Tile("science_table.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "28":
                    tiles.append(Tile("science_table2.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "29":
                    tiles.append(Tile("small_table.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "30":
                    tiles.append(Tile("tile_10_4.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == "31":
                    tiles.append(Tile("window_wall.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles



        