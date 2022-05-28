import pygame
import csv
import os
import json

import utils
from utils import display, display_scroll

tilenames = ['base.png', 'grass.png', 'flower1.png', 'flower2.png', 'road_corner_SE.png',
             'road_corner_SW.png', 'road_corner_NW.png', 'road_corner_NE.png', 'road_E.png', 'road_S.png',
             'road_W.png', 'road_N.png', 'road_full_1.png', 'road_full_2.png', 'road_NW.png',
             'road_NE.png', 'road_SE.png', 'road_SW.png']


class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        pygame.transform.scale(image, (32, 32))
        return image


class Tile:
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.texture = pygame.transform.scale(image, (64, 64))

    def draw(self):
        display.blit(self.texture, (self.x + display_scroll[0], self.y + display_scroll[1]))


class TileMap:
    def __init__(self, filename, spritesheet):
        self.tile_size = 64
        self.models = []
        self.spritesheet = spritesheet
        self.fill_models()
        self.tiles = self.load_tiles(filename)
        self.map_w = 0
        self.map_h = 0

    def draw_map(self):
        for tile in self.tiles:
            tile.draw()

    def fill_models(self):
        for tilename in tilenames:
            self.models.append(self.spritesheet.parse_sprite(tilename))

    def read_csv(self, filename):
        tmap = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data)
            for row in data:
                tmap.append(list(row))
        self.map_h = len(tmap)
        self.map_w = len(tmap[0])
        return tmap

    def load_tiles(self, filename):
        tiles = []
        tmap = self.read_csv(filename)
        x, y = 0, 0
        for row in tmap:
            x = 0
            for tile in row:
                tiles.append(Tile(self.models[int(tile)], x * self.tile_size - self.map_w,
                                  y * self.tile_size - self.map_h))
                x += 1
            y += 1
        return tiles
