
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Map:

    def __init__(self, lines: List[str]) -> None:
        self.lines = [list(l) for l in lines]
        self.nr = len(lines)
        self.nc = len(lines[0])
        self.s = self.find_s()
        self.sr = self.s[0]
        self.sc = self.s[1]

        sl = self.find_letter_s()
        debug(f"The S letter is {sl} in {self.sr},{self.sc}")
        self.lines[self.sr][self.sc] = sl


    def connected(self, row, col):
        pipe = self.lines[row][col]
        # debug(f"Checking connection for <{row},{col}> -> {pipe}")

        if pipe == "|":
            return (row+1, col, row-1, col)

        elif pipe == "-":
            return (row, col-1, row, col+1)

        elif pipe == "L":
            return (row, col+1, row-1, col)

        elif pipe == "J":
            return (row, col-1, row-1, col)

        elif pipe == "7":
            return (row, col-1, row+1, col)

        elif pipe == "F":
            return (row, col+1, row+1, col)

        return None


    def find_s(self):
        for i in range(self.nr):
            for j in range(self.nc):
                if self.lines[i][j] == "S":
                    return (i, j)


    def find_letter_s(self):
        neig = self.neighbors(self.sr, self.sc)
        north = False
        south = False
        west = False
        east = False

        if self.sr > 0:
            c = self.lines[self.sr-1][self.sc]
            if c == "|" or c == "7" or c == "F":
                north = True

        if self.sr < self.nr - 1:
            c = self.lines[self.sr+1][self.sc]
            if c == "|" or c == "L" or c == "J":
                south = True

        if self.sc > 0:
            c = self.lines[self.sr][self.sc-1]
            if c == "-" or c == "L" or c == "F":
                west = True

        if self.sc < self.nc - 1:
            c = self.lines[self.sr][self.sc+1]
            if c == "-" or c == "7" or c == "J":
                east = True

        if north and south:
            return "|"
        elif north and east:
            return "L"
        elif north and west:
            return "J"
        elif south and east:
            return "F"
        elif south and west:
            return "7"
        else:
            return "-"


    def neighbors(self, row, col):
        n = []
        if row > 0:
            n.append((row-1, col))
        if row < self.nr - 1:
            n.append((row+1, col))
        if col > 0:
            n.append((row, col-1))
        if col < self.nc - 1:
            n.append((row, col+1))
        return n


    def count_loop(self):
        old_r, old_c = self.s
        r, c = self.s
        counter = 0
        while True:
            counter += 1

            debug(f"In step {counter} moving from {r},{c}")

            r1, c1, r2, c2 = self.connected(r, c)

            if r1 == old_r and c1 == old_c:
                old_r, old_c = r, c
                r, c = r2, c2
            else:
                old_r, old_c = r, c
                r, c = r1, c1

            if r == self.sr and c == self.sc:
                break

        return counter


    def get_loop(self):
        loop = [self.s]

        old_r, old_c = self.s
        r, c = self.s
        while True:
            r1, c1, r2, c2 = self.connected(r, c)

            if r1 == old_r and c1 == old_c:
                old_r, old_c = r, c
                r, c = r2, c2
            else:
                old_r, old_c = r, c
                r, c = r1, c1

            if r == self.sr and c == self.sc:
                break
            else:
                loop.append((r, c))

        return loop


    def remove_all_except_loop(self):
        loop = self.get_loop()

        for i in range(self.nr):
            for j in range(self.nc):
                if (i,j) not in loop:
                    self.lines[i][j] = "."


    def modify_cell(self, row, col, out):
        if self.lines[row][col] == ".":
            self.lines[row][col] = out


    def modify_neigs(self, row, col, direction):

        pipe = self.lines[row][col]

        if pipe == "|":
            if direction == "N":
                self.modify_cell(row, col-1, "O")
                self.modify_cell(row, col+1, "I")
            else:
                self.modify_cell(row, col-1, "I")
                self.modify_cell(row, col+1, "O")

        if pipe == "-":
            if direction == "E":
                self.modify_cell(row-1, col, "O")
                self.modify_cell(row+1, col, "I")
            else:
                self.modify_cell(row-1, col, "I")
                self.modify_cell(row+1, col, "O")

        if pipe == "L":
            if direction == "W":
                self.modify_cell(row+1, col, "O")
                self.modify_cell(row, col-1, "O")
            else:
                self.modify_cell(row+1, col, "I")
                self.modify_cell(row, col-1, "I")

        if pipe == "J":
            if direction == "S":
                self.modify_cell(row+1, col, "O")
                self.modify_cell(row, col+1, "O")
            else:
                self.modify_cell(row+1, col, "I")
                self.modify_cell(row, col+1, "I")

        if pipe == "7":
            if direction == "E":
                self.modify_cell(row-1, col, "O")
                self.modify_cell(row, col+1, "O")
            else:
                self.modify_cell(row-1, col, "I")
                self.modify_cell(row, col+1, "I")

        if pipe == "F":
            if direction == "N":
                self.modify_cell(row-1, col, "O")
                self.modify_cell(row, col-1, "O")
            else:
                self.modify_cell(row-1, col, "I")
                self.modify_cell(row, col-1, "I")


    def expand(self):
        expanded = 1
        while expanded:
            expanded = 0
            for i in range(self.nr):
                for j in range(self.nc):
                    if self.lines[i][j] == "I":
                        for r, c in self.neighbors(i, j):
                            if self.lines[r][c] == ".":
                                expanded += 1
                                self.lines[r][c] = "I"
                    elif self.lines[i][j] == "O":
                        for r, c in self.neighbors(i, j):
                            if self.lines[r][c] == ".":
                                expanded += 1
                                self.lines[r][c] = "O"



    def modify_loop(self):
        loop = self.get_loop()

        r, c = loop[0]
        pipe = self.lines[r][c]

        # Assuming pipe of S is always F
        direction = "N"

        while True:

            self.modify_neigs(r, c, direction)
            direction = self.get_next_direction(r, c, direction)
            r, c = self.get_cell_from_direction(r, c, direction)

            if r == self.sr and c == self.sc:
                break


    def get_cell_from_direction(self, row, col, direction):
        if direction == "N":
            return (row-1, col)
        elif direction == "S":
            return (row+1, col)
        elif direction == "E":
            return (row, col+1)
        elif direction == "W":
            return (row, col-1)

    def get_next_direction(self, row, col, direction):

        pipe = self.lines[row][col]

        if pipe == "|":
            if direction == "N":
                return "N"
            else:
                return "S"

        elif pipe == "-":
            if direction == "E":
                return "E"
            else:
                return "W"

        elif pipe == "L":
            if direction == "S":
                return "E"
            else:
                return "N"

        elif pipe == "J":
            if direction == "S":
                return "W"
            else:
                return "N"

        elif pipe == "7":
            if direction == "E":
                return "S"
            else:
                return "W"

        elif pipe == "F":
            if direction == "N":
                return "E"
            else:
                return "S"

        error(f"ERROR IN DIRECTION:  <{row},{col}>  {pipe}  {direction}")

    def remove_loop(self):
        loop = self.get_loop()

        for r, c in loop:
            self.lines[r][c] = "·"


    def count_char(self, c):
        counter = 0
        for i in range(self.nr):
            for j in range(self.nc):
                if self.lines[i][j] == c:
                    counter += 1
        return counter


    def __str__(self) -> str:
        return '\n'.join([''.join(x) for x in self.lines])





################################################################################
def solution_a(inp):
    return Map(inp).count_loop()//2


################################################################################
def solution_b(inp):
    # Whit these the loop never gets the map limit
    inp = ["."*len(inp[0])] + inp + ["."*len(inp[0])]
    inp = ["." + i + "." for i in inp]
    m = Map(inp)

    m.remove_all_except_loop()
    debug(m)
    debug("")
    m.modify_loop()
    debug(m)
    debug("")
    m.expand()
    debug(m)
    debug("")
    m.modify_loop()
    debug(m)

    debug(f"Is: {m.count_char('I')}")
    debug(f"Os: {m.count_char('O')}")

    return min(m.count_char("I"), m.count_char("O"))
