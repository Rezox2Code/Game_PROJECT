class Tile:
    def __init__(self, name: str):
        self.name = name

    def is_joker(self):
        return self.name.startswith("joker")

    def value(self):
        if self.is_joker():
            return None
        return int(self.name.split("_")[0])

    def color(self):
        if self.is_joker():
            return None
        return self.name.split("_")[1]

    def to_dict(self):
        return {"name": self.name}

    @staticmethod
    def from_dict(data):
        return Tile(data["name"])

    def __repr__(self):
        return self.name
