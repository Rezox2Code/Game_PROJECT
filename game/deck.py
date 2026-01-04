import random
from game.tile import Tile

class Deck:
    def __init__(self, double_set=True):
        self.tiles = self._generate_tiles(double_set)
        random.shuffle(self.tiles)

    def _generate_tiles(self, double_set):
        colors = ["bleu", "noir", "orange", "rouge"]
        base_tiles = []

        for n in range(1, 14):
            for c in colors:
                base_tiles.append(Tile(f"{n}_{c}"))

        base_tiles.append(Tile("joker_black"))
        base_tiles.append(Tile("joker_red"))

        if double_set:
            base_tiles = base_tiles * 2

        return base_tiles

    def draw(self):
        return self.tiles.pop() if self.tiles else None

    def to_dict(self):
        return [tile.to_dict() for tile in self.tiles]

    @staticmethod
    def from_dict(data):
        deck = Deck(False)
        deck.tiles = [Tile.from_dict(t) for t in data]
        return deck
