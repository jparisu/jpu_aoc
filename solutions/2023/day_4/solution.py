
# Load utils
import sys
sys.path.append('../../')
from utils import *


################################################################################
class Card:

    def __init__(self, line):
        line = line.split(":")[-1].strip()
        w, c = line.split("|")

        self.wining = [int(x) for x in w.split()]
        self.have = [int(x) for x in c.split()]

        self.wining.sort()
        self.have.sort()

    def value(self):
        l = self.wins()
        if l == 0:
            return 0
        else:
            return 2**(l-1)

    def wins(self):
        return len([x for x in self.have if x in self.wining])


def solution_a(inp):

    return sum([Card(line).value() for line in inp])


################################################################################
def solution_b(inp):

    cards = [1 for _ in range(len(inp))]

    for i, card in enumerate(inp):
        w = Card(card).wins()
        for j in range(1, w+1):
            cards[i+j] += cards[i]

    return sum(cards)
