
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Direction(Enum):
    U = 3
    R = 0
    D = 1
    L = 2

class Board:

    def __init__(self, inp):


        self.disperse_matrix = set(self.parse_input(inp))
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.in_point = (1, 1)

        for x, y in self.disperse_matrix:
            if x < self.min_x:
                self.min_x = x
            if x > self.max_x:
                self.max_x = x
            if y < self.min_y:
                self.min_y = y
            if y > self.max_y:
                self.max_y = y

    def parse_input(self, inp):

        disperse_matrix = [(0, 0)]
        current = (0, 0)

        for line in inp:
            dir, n, color = line.split()
            dir = Direction[dir]
            n = int(n)
            color = color[2:-1]

            for i in range(n):
                if dir == Direction.U:
                    current = (current[0]-1,current[1])
                elif dir == Direction.R:
                    current = (current[0],current[1]+1)
                elif dir == Direction.D:
                    current = (current[0]+1,current[1])
                elif dir == Direction.L:
                    current = (current[0],current[1]-1)
                disperse_matrix.append(current)

        return disperse_matrix

    def __str__(self) -> str:
        s = ""
        for i in range(self.min_x, self.max_x+1):
            for j in range(self.min_y, self.max_y+1):
                if (i,j) in self.disperse_matrix:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        return s

    def get_neigs(point) -> List[Tuple[int, int]]:
        x, y = point

        return [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1),
        ]

    def fill_n(self) -> Set[Tuple[int, int]]:

        new_points = {self.in_point}
        points = set()

        while len(new_points) > 0:
            p = new_points.pop()

            if p[0] < self.min_x or p[0] > self.max_x or p[1] < self.min_y or p[1] > self.max_y:
                error(f"Out of range: {p}")
                break

            points.add(p)

            for n in Board.get_neigs(p):
                if n not in points and n not in self.disperse_matrix:
                    new_points.add(n)

        return points


################################################################################
def solution_a(inp):
    b = Board(inp)
    debug(str(b))
    return len(b.fill_n()) + len(b.disperse_matrix)


################################################################################
def parse1(inp):
    movements = []
    for l in inp:
        dir, n, _ = l.split()
        movements.append((Direction[dir], int(n)))
    return movements


def parse2(inp):
    movements = []
    for l in inp:
        dir, n, color = l.split()
        dir = Direction(int(color[-2]))
        n = int(color[2:-2], 16)
        movements.append((dir, n))
    return movements


def x_limits(movements):
    current = 0
    x_min = 0
    x_max = 0

    for dir, steps in movements:
        if dir == Direction.R:
            current = current + steps
            x_max = max(x_max, current)
        if dir == Direction.L:
            current = current - steps
            x_min = min(x_min, current)

    return x_max, x_min


def y_limits(movements):
    current = 0
    y_min = 0
    y_max = 0

    return y_max, y_min


def square_size(movements):
    x_max, x_min = x_limits(movements)
    y_max, y_min = y_limits(movements)

    return (x_max - x_min + 1) * (y_max - y_min + 1)


def add_line_to_lines(ini, fin, lines):
    for i in range(len(lines)):
        if lines[i][0] > ini:
            lines.insert(i, (ini, fin))
            return lines
    lines.append((ini, fin))
    return lines


def add_line_to_whole_lines(ini, fin, x, lines: List):
    for i in range(len(lines)):
        if lines[i][0] == x:
            lines[i][1] = add_line_to_lines(ini, fin, lines[i][1])
            return lines
        elif lines[i][0] > x:
            lines.insert(i, [x, [(ini, fin)]])
            return lines
    lines.append([x, [(ini, fin)]])
    return lines


def calculate_with_line(y, lines):
    ins = 0
    is_in = False
    is_in_line = False
    last = 0
    last_line_came_from_above = False

    for i in range(len(lines)):
        x, l = lines[i]
        for j in range(len(l)):
            line_ini, line_fin = l[j]
            ins += 1

            if y == line_ini:

                if is_in_line:

                    if last_line_came_from_above:

                        if is_in:
                            # Case 7
                            is_in = False
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                        else:
                            # Case 2
                            is_in = True
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                    else:

                        if is_in:
                            # Case 4
                            is_in = True
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                        else:
                            # Case 0
                            is_in = False
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                else:

                    if is_in:
                        # Case 13
                        is_in = True
                        ins += x - last - 1
                        last = x
                        is_in_line = True
                        last_line_came_from_above = False

                    else:
                        # Case 11
                        is_in = False
                        last = x
                        is_in_line = True
                        last_line_came_from_above = False


            elif y == line_fin:

                if is_in_line:

                    if last_line_came_from_above:

                        if is_in:
                            # Case 5
                            is_in = True
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                        else:
                            # Case 1
                            is_in = False
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                    else:

                        if is_in:
                            # Case 6
                            is_in = False
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                        else:
                            # Case 3
                            is_in = True
                            ins += x - last - 1
                            last = x
                            is_in_line = False

                else:

                    if is_in:
                        # Case 12
                        is_in = True
                        ins += x - last - 1
                        last = x
                        is_in_line = True
                        last_line_came_from_above = True

                    else:
                        # Case 10
                        is_in = False
                        last = x
                        is_in_line = True
                        last_line_came_from_above = True

            elif line_ini < y and line_fin > y:

                if is_in:
                    # Case 9
                    is_in = False
                    ins += x - last - 1
                    is_in_line = False
                    last = x

                else:
                    # Case 8
                    is_in = True
                    last = x
                    is_in_line = False
                    last = x

            else:
                # Case X
                ins -= 1

    return ins


def calculate_without_line(y, lines):
    ins = 0
    is_in = False
    last = 0
    for i in range(len(lines)):
        x, l = lines[i]
        for j in range(len(l)):
            if l[j][0] < y and l[j][1] > y:
                if is_in:
                    is_in = False
                    ins += x - last + 1
                else:
                    is_in = True
                    last = x
    return ins


def solution(movements):

    x = 0
    y = 0
    vertical_lines = []
    horizontal_lines = []
    x_points = set()
    y_points = set()

    for dir, steps in movements:
        if dir == Direction.U:
            vertical_lines = add_line_to_whole_lines(y, y + steps, x, vertical_lines)
            y = y + steps
            y_points.add(y)
        if dir == Direction.D:
            vertical_lines = add_line_to_whole_lines(y - steps, y, x, vertical_lines)
            y = y - steps
            y_points.add(y)
        if dir == Direction.R:
            horizontal_lines = add_line_to_whole_lines(x, x + steps, y, horizontal_lines)
            x = x + steps
            x_points.add(x)
        if dir == Direction.L:
            horizontal_lines = add_line_to_whole_lines(x - steps, x, y, horizontal_lines)
            x = x - steps
            x_points.add(x)

    x_min = min(x_points)
    x_max = max(x_points)
    y_min = min(y_points)
    y_max = max(y_points)

    y_points = list(y_points)
    y_points.sort()

    debug(f"X: < {x_min} , {x_max} >  -  {x_max-x_min}")
    debug(f"Y: < {y_min} , {y_max} >  -  {y_max-y_min}")
    debug(f"V Lines: {vertical_lines}")
    debug(f"H Lines: {horizontal_lines}")
    debug(f"Y Points: {y_points}")


    result = 0

    for i in range(len(y_points) - 1):
        h_line = y_points[i]

        squares_in_line = calculate_with_line(h_line, vertical_lines)
        debug(f"Line with points: {h_line}  is: {squares_in_line}")

        squares_in_middle = 0
        times = y_points[i+1] - h_line - 1

        if y_points[i+1] != h_line + 1:
            squares_in_middle = calculate_without_line(h_line + 1, vertical_lines)
            debug(f"Line without points in: {h_line+1}  is: {squares_in_middle}  for {times}  times")

        result += squares_in_line + squares_in_middle * (times)

    result += calculate_with_line(y_points[-1], vertical_lines)

    return result


def debug_show(movements):
    return solution(movements)

################################################################################
# def solution_a(inp):
#     movements = parse1(inp)
#     return solution(movements)

################################################################################
def solution_b(inp):
    movements = parse2(inp)
    return solution(movements)
