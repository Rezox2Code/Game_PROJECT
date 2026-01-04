class Table:
    def __init__(self):
        self.combinations = []

    def add_combination(self, combo):
        self.combinations.append(combo)

    def to_dict(self):
        return self.combinations

    @staticmethod
    def from_dict(data):
        t = Table()
        t.combinations = data
        return t

    def __repr__(self):
        return str(self.combinations)
