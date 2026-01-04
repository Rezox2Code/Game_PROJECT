import json
from game.deck import Deck
from game.player import Player
from game.table import Table

class Game:
    def __init__(self, players_names):
        self.deck = Deck(double_set=True)
        self.players = [Player(name) for name in players_names]
        self.table = Table()
        self.current_player = 0

        for p in self.players:
            for _ in range(14):
                p.draw_tile(self.deck.draw())

    def next_turn(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def save(self, path="data/game_state.json"):
        data = {
            "deck": self.deck.to_dict(),
            "players": [p.to_dict() for p in self.players],
            "table": self.table.to_dict(),
            "current_player": self.current_player
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load(path="data/game_state.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game = Game([])
        game.deck = Deck.from_dict(data["deck"])
        game.players = [Player.from_dict(p) for p in data["players"]]
        game.table = Table.from_dict(data["table"])
        game.current_player = data["current_player"]
        return game
