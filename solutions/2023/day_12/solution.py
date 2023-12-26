
# Load utils
import sys
sys.path.append('../../')
from utils import *

import itertools

################################################################################
parse_dict = {
    "?": -1,
    ".": 0,
    "#": 1
}

class Row:

    def __init__(self, line=None, gears=None, values=None, multiplies=False) -> None:

        if line is not None:
            g, v = line.split()
            self.gears = Row.parse(g)
            self.values = list(map(int, v.split(",")))
        else:
            self.gears = gears
            self.values = values

        if multiplies:
            self.gears = self.gears + [-1] + self.gears + [-1] + self.gears + [-1] + self.gears + [-1] + self.gears
            self.values = self.values + self.values + self.values + self.values + self.values

        self.gears += [0]
        # debug(f"Created Row: {self}")

    def parse(line):
        return [parse_dict[x] for x in line]

    def count_unknown(self) -> int:
        return sum([1 for x in self.gears if x == -1])

    def is_valid(self) -> bool:
        count = -1
        index = -1
        counting = False

        for c in self.gears:
            if c == 1:
                if not counting:
                    counting = True
                    count = 1
                    index += 1
                    if index >= len(self.values):
                        return False
                else:
                    count += 1

            else:
                if counting:
                    if self.values[index] != count:
                        return False
                    counting = False

        return index == len(self.values)-1

    def generate_row_with_permutation(self, perm) -> "Row":
        gears = list(self.gears)
        index = 0

        for c in perm:
            while gears[index] != -1:
                index += 1
            gears[index] = c

        return Row(None, gears, self.values)

    def count_possible_permutations(self) -> int:
        n = self.count_unknown()
        valid = 0
        for perm in itertools.product([0, 1], repeat=n):
            if self.generate_row_with_permutation(perm).is_valid():
                debug(f"Permutation {perm} for {self}  is valid")
                valid += 1
        debug(f"Permutations for {self}  are: {valid}")
        return valid

    def __str__(self):
        s = ""
        for c in self.gears:
            if c == -1:
                s += "?"
            elif c == 0:
                s += "."
            else:
                s += "#"
        return f"< {s} >  {self.values}"

################################################################################
def solution_a(inp):
    return sum([Row(line).count_possible_permutations() for line in inp])

################################################################################
class BetterRow:


    def __init__(self, gears, values) -> None:
        self.gears = [0] + gears
        self.values = values
        self.cache = {}


    def __str__(self):
        s = ""
        for c in self.gears:
            if c == -1:
                s += "?"
            elif c == 0:
                s += "."
            else:
                s += "#"
        return f"< {s} >  {self.values}"


    def calculate(self, gears_index, values_index, precounting=0):

        args = (gears_index, values_index, precounting)
        if args in self.cache:
            return self.cache[args]

        result = 0
        if gears_index < 0:
            if values_index < 0:
                result = 1
            else:
                result = 0

        # When finding a .
        elif self.gears[gears_index] == 0:

            if precounting == 0:
                result = self.calculate(gears_index-1, values_index, 0)
            else:
                if self.values[values_index] != precounting:
                    result = 0
                else:
                    result = self.calculate(gears_index-1, values_index-1, 0)

        # When finding a #
        elif self.gears[gears_index] == 1:

            if values_index < 0:
                result = 0
            elif precounting + 1 > self.values[values_index]:
                result = 0
            else:
                result = self.calculate(gears_index-1, values_index, precounting + 1)

        # When finding a ?
        else:

            # add .
            value_0 = 0
            if precounting == 0:
                value_0 = self.calculate(gears_index-1, values_index, precounting)
            else:
                if self.values[values_index] != precounting:
                    value_0 = 0
                else:
                    value_0 = self.calculate(gears_index-1, values_index-1, 0)

            # add #
            value_1 = 0
            if values_index < 0:
                value_1 = 0
            elif precounting + 1 > self.values[values_index]:
                value_1 = 0
            else:
                value_1 = self.calculate(gears_index-1, values_index, precounting + 1)

            result = value_0 + value_1

            # debug(f"{args} Finding in  . <{value_0}>  and  # <{value_1}>")

        # debug(f"Calculating result for args: {args} :  {result}")

        self.cache[args] = result

        return result


################################################################################
def solution_b(inp):
    result = 0
    for i in inp:

        gears = []
        g = [parse_dict[x] for x in i.split()[0]]
        for _ in range(5):
            gears += g + [-1]
        gears = gears[:-1]

        values = []
        v = list(map(int, i.split()[1].split(",")))
        for _ in range(5):
            values += v &

        r = BetterRow(gears, values)
        c = r.calculate(len(gears), len(values)-1)
        debug(f"Generated BetterRow: {r}  with value: {c}")
        # debug(f"{r.cache}")
        # debug("")
        result += c

    return result
