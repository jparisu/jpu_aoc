
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
def char_to_card(c: str, joker: bool = False) -> int:
    if char_is_numeric(c):
        return int(c)
    elif c == "T":
        return 10
    elif c == "J":
        if joker:
            return 0
        else:
            return 11
    elif c == "Q":
        return 12
    elif c == "K":
        return 13
    elif c == "A":
        return 14
    else:
        error(f"Char {c} incorrect")

class Hand:

    def __init__(self, line: str, cards=None):
        if not cards:
            chars, v = line.split()
            self.cards = [char_to_card(c) for c in chars]
            self.real_cards = self.cards
            self.v = int(v)
        else:
            self.cards = cards
            self.real_cards = cards
            self.v = 0

    def __lt__(self, other: "Hand") -> bool:

        this_prior = self._hand_priority()
        other_prior = other._hand_priority()

        if this_prior < other_prior:
            return True
        elif this_prior > other_prior:
            return False

        for i in range(len(self.real_cards)):
            if self.real_cards[i] < other.real_cards[i]:
                return True
            elif self.real_cards[i] > other.real_cards[i]:
                return False
        return False

    def _hand_priority(self) -> int:

        d = count_values_to_dict(self.cards)
        vs = d.values()

        # Repoker
        if len(d) == 1:
            return 7

        # Poker
        elif 4 in vs:
            return 6

        # Full House
        elif len(d) == 2:
            return 5

        # Third
        elif 3 in vs:
            return 4

        # Double pair
        elif len(d) == 3:
            return 3

        # Pair
        elif len(d) == 4:
            return 2

        # High card
        else:
            return 1

    def __str__(self) -> str:
        return f"< {self.cards} >  {self.v}"



################################################################################
def solution_a(inp):
    cards = sorted([Hand(i) for i in inp])
    return sum([(i+1)*cards[i].v for i in range(len(cards))])

"""
250367404 - too low
"""

################################################################################
import itertools

class JokerHand(Hand):

    def __init__(self, line: str):
        chars, v = line.split()
        self.real_cards = [char_to_card(c, True) for c in chars]
        self.cards = self.real_cards
        self.v = int(v)

        self.cards = self.get_winner_hand()

    def get_winner_hand(self):
        if 0 not in self.real_cards:
            return self.real_cards

        # Count 1s in self.real_cards
        d = count_values_to_dict(self.real_cards)
        all_possibilities = set()

        for perm in itertools.product(range(2, 15), repeat=d[0]):
            hand = list(self.cards)
            j = 0
            for i in range(len(hand)):
                if hand[i] == 0:
                    hand[i] = perm[j]
                    j += 1
            all_possibilities.add(Hand(line="", cards=hand))

        debug(f"For cards {self.cards} there are these possibilities:")
        for p in all_possibilities:
            debug(f"  {p}")

        return max(all_possibilities).cards



################################################################################
def solution_b(inp):
    cards = sorted([JokerHand(i) for i in inp])
    return sum([(i+1)*cards[i].v for i in range(len(cards))])
