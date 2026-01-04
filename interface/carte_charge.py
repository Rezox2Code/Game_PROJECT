import pygame
import os

ASSETS_PATH = "interface/asset"
CARD_SIZE = (80, 120)

class CardLoader:
    def __init__(self):
        self.cache = {}

    def get(self, tile_name):
        if tile_name not in self.cache:
            path = os.path.join(ASSETS_PATH, f"{tile_name}.png")
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, CARD_SIZE)
            self.cache[tile_name] = image
        return self.cache[tile_name]
