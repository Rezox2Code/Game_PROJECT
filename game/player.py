from game.tile import Tile

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_tile(self, tile):
        if tile:
            self.hand.append(tile)

    def play_tiles(self, tiles):
        for t in tiles:
            self.hand.remove(t)

    def to_dict(self):
        return {
            "name": self.name,
            "hand": [t.to_dict() for t in self.hand]
        }

    @staticmethod
    def from_dict(data):
        p = Player(data["name"])
        p.hand = [Tile.from_dict(t) for t in data["hand"]]
        return p

    def __repr__(self):
        return f"{self.name} : {self.hand}"
