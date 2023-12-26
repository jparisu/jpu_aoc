
# Load utils
import sys
sys.path.append('../../')
from utils import *

import copy

################################################################################
class Board:

    def __init__(self, lines):
        self.rows = []
        for line in lines:
            self.rows.append([])
            for c in line:
                if c == ".":
                    self.rows[-1].append(0)
                elif c == "O":
                    self.rows[-1].append(1)
                else:
                    self.rows[-1].append(2)
        self.nr = len(self.rows)
        self.nc = len(self.rows[0])


    def __str__(self) -> str:
        s = ""
        for r in self.rows:
            for c in r:
                if c == 0:
                    s += "."
                elif c == 1:
                    s += "O"
                else:
                    s += "#"
            s += "\n"
        return s


    def get_value(self):
        res = 0
        for i, r in enumerate(self.rows):
            for c in r:
                if c == 1:
                    res += self.nr - i
        return res


    def move_north(self):
        moved = 0
        for i in range(1, self.nr):
            for j in range(self.nc):
                if self.rows[i][j] == 1:
                    if self.rows[i-1][j] == 0:
                        self.rows[i-1][j] = 1
                        self.rows[i][j] = 0
                        moved = 1
        if moved > 0:
            self.move_north()


    def move_south(self):
        moved = 0
        for i in range(self.nr-2, -1, -1):
            for j in range(self.nc):
                if self.rows[i][j] == 1:
                    if self.rows[i+1][j] == 0:
                        self.rows[i+1][j] = 1
                        self.rows[i][j] = 0
                        moved = 1
        if moved > 0:
            self.move_south()


    def move_west(self):
        moved = 0
        for j in range(1, self.nc):
            for i in range(self.nr):
                if self.rows[i][j] == 1:
                    if self.rows[i][j-1] == 0:
                        self.rows[i][j-1] = 1
                        self.rows[i][j] = 0
                        moved = 1
        if moved > 0:
            self.move_west()


    def move_east(self):
        moved = 0
        for j in range(self.nc-2,-1,-1):
            for i in range(self.nr):
                if self.rows[i][j] == 1:
                    if self.rows[i][j+1] == 0:
                        self.rows[i][j+1] = 1
                        self.rows[i][j] = 0
                        moved = 1
        if moved > 0:
            self.move_east()


    def move_cycle(self):
        self.move_north()
        self.move_west()
        self.move_south()
        self.move_east()


    def move_cycles(self, n: int):
        cache = []
        cached = False
        i = 0
        while i < n:
            self.move_north()
            self.move_west()
            self.move_south()
            self.move_east()

            s = str(self)

            if not cached:
                for j, c in enumerate(cache):
                    if s == c:
                        debug(f"Cached {i} with {j}:\n{s}")

                        cached = True
                        loop = i - j
                        while i + loop < n:
                            i += loop

                cache.append(s)

            debug(f"{i}:\n{s}")
            i += 1


################################################################################
def solution_a(inp):
    b = Board(inp)
    debug(f"{b}")
    b.move_north()
    debug(f"{b}")
    return b.get_value()

################################################################################

################################################################################
def solution_b(inp):
    b = Board(inp)
    debug(f"{b}")
    N = 1000000000
    # N = 200
    b.move_cycles(N)
    debug(f"{b}")
    return b.get_value()
