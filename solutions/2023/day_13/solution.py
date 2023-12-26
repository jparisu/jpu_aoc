
# Load utils
import sys
sys.path.append('../../')
from utils import *

RAW_INPUT = True

################################################################################
class Map:

    def __init__(self, lines):
        self.rows = []
        for l in lines:
            self.rows.append([])
            for c in l.strip():
                if c == ".":
                    self.rows[-1].append(0)
                else:
                    self.rows[-1].append(1)
        self.nr = len(self.rows)
        self.nc = len(self.rows[0])


    def get_vertical_line(self) -> int:

        for col in range(1, self.nc):
            symmetry = True
            distance = min(col, self.nc - col)
            for row in range(self.nr):
                i = col - distance
                j = col + distance - 1
                while i < j:
                    if self.rows[row][i] != self.rows[row][j]:
                        symmetry = False
                        break
                    i += 1
                    j -= 1

                if not symmetry:
                    break

            if symmetry:
                return col

        return 0


    def get_horizontal_line(self) -> int:

        for row in range(1, self.nr):
            symmetry = True
            distance = min(row, self.nr - row)
            for col in range(self.nc):
                i = row - distance
                j = row + distance - 1
                while i < j:
                    if self.rows[i][col] != self.rows[j][col]:
                        symmetry = False
                        break
                    i += 1
                    j -= 1

                if not symmetry:
                    break

            if symmetry:
                return row

        return 0


    def get_value(self) -> int:
        return self.get_horizontal_line() * 100 + self.get_vertical_line()


    def get_vertical_line_with_change(self):

        row_ff = -1
        col_ff = -1
        col_solve = -1
        erros_1 = 0

        for col in range(1, self.nc):

            symmetry_failure = 0
            row_f = 0
            col_f = 0
            distance = min(col, self.nc - col)

            for row in range(self.nr):
                i = col - distance
                j = col + distance - 1
                while i < j:
                    if self.rows[row][i] != self.rows[row][j]:
                        symmetry_failure += 1
                        row_f = row
                        col_f = i
                    i += 1
                    j -= 1

            if symmetry_failure == 1:
                erros_1 += 1
                row_ff = row_f
                col_ff = col_f
                col_solve = col

        if erros_1 > 1:
            error(f"More than 1 error!")

        return row_ff, col_ff, col_solve


    def get_horizontal_line_with_change(self) -> int:

        row_ff = -1
        col_ff = -1
        row_solve = -1
        erros_1 = 0

        for row in range(1, self.nr):

            symmetry_failure = 0
            row_f = 0
            col_f = 0
            distance = min(row, self.nr - row)

            for col in range(self.nc):
                i = row - distance
                j = row + distance - 1
                while i < j:
                    if self.rows[i][col] != self.rows[j][col]:
                        symmetry_failure += 1
                        row_f = i
                        col_f = col
                    i += 1
                    j -= 1

            if symmetry_failure == 1:
                erros_1 += 1
                row_ff = row_f
                col_ff = col_f
                row_solve = row

        if erros_1 > 1:
            error(f"More than 1 error!")

        return row_ff, col_ff, row_solve


    def get_value_2(self) -> int:
        r1, c1, v1 = self.get_horizontal_line_with_change()
        r, c, v = self.get_vertical_line_with_change()

        if v == -1:
            return v1 * 100
        else:
            return v



    def __str__(self) -> str:
        s = ""
        for r in self.rows:
            for c in r:
                s += str(c)
            s += "\n"
        return s

################################################################################
def solution_a(inp):

    lines = []
    maps = []

    for i in inp:
        if i == "\n":
            maps.append(Map(lines))
            lines = []
        else:
            lines.append(i)

    maps.append(Map(lines))

    return sum([x.get_value() for x in maps])


################################################################################

################################################################################
def solution_b(inp):

    lines = []
    maps = []

    for i in inp:
        if i == "\n":
            maps.append(Map(lines))
            lines = []
        else:
            lines.append(i)

    maps.append(Map(lines))

    # for m in maps:
    #     debug(f"{m}")
    #     debug(f"{m.get_vertical_line_with_change()}")
    #     debug(f"{m.get_horizontal_line_with_change()}")
    #     debug("")

    return sum([x.get_value_2() for x in maps])
