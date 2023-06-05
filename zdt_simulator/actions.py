from enum import Enum


class Action(Enum):
    AA = "Aggressive Ask"
    AB = "Aggressive Bid"
    N = "Neutral"

    def __lt__(self, other):
        return self.name < other.name

    def __le__(self, other):
        return self.name <= other.name

    def __ge__(self, other):
        return self.name >= other.name

    def __gt__(self, other):
        return self.name > other.name

    def __str__(self):
        return self.name
