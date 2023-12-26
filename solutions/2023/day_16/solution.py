
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Direction:
    Up = 0
    Right = 1
    Down = 2
    Left = 3

class Mirrors:
    Non = 0
    Horizontal = 1
    Vertical = 2
    RightUp = 3
    RightDown = 4


class LightBeam:

    def __init__(self, row: int, col: int, direction: Direction):
        self.row = row
        self.col = col
        self.direction = direction


class Board:

    def __init__(self, lines):
        self.matrix = []
        for line in lines:
            self.matrix.append([])
            for c in line:
                if c == "/":
                    self.matrix[-1].append([Mirrors.RightUp, False])
                elif c == "\\":
                    self.matrix[-1].append([Mirrors.RightDown, False])
                elif c == "-":
                    self.matrix[-1].append([Mirrors.Horizontal, False])
                elif c == "|":
                    self.matrix[-1].append([Mirrors.Vertical, False])
                else:
                    self.matrix[-1].append([Mirrors.Non, False, set()])

        self.nr = len(self.matrix)
        self.nc = len(self.matrix[0])
        self.lights = [LightBeam(0,-1,Direction.Right)]


    def move_light(self, light: LightBeam) -> List[LightBeam]:
        row = light.row
        col = light.col
        if light.direction == Direction.Up:
            row -= 1
        elif light.direction == Direction.Down:
            row += 1
        elif light.direction == Direction.Left:
            col -= 1
        elif light.direction == Direction.Right:
            col += 1

        if row < 0 or row >= self.nr or col < 0 or col >= self.nc:
            return []

        self.matrix[row][col][1] = True
        space = self.matrix[row][col]
        c = self.matrix[row][col][0]

        if c == Mirrors.Non:
            if light.direction in space[2]:
                return []
            else:
                space[2].add(light.direction)
                return [LightBeam(row, col, light.direction)]

        else:

            if light.direction == Direction.Up:
                if c == Mirrors.Vertical:
                    return [LightBeam(row, col, Direction.Up)]
                elif c == Mirrors.RightDown:
                    return [LightBeam(row, col, Direction.Left)]
                elif c == Mirrors.RightUp:
                    return [LightBeam(row, col, Direction.Right)]
                else:
                    return [LightBeam(row, col, Direction.Left), LightBeam(row, col, Direction.Right)]

            if light.direction == Direction.Down:
                if c == Mirrors.Vertical:
                    return [LightBeam(row, col, Direction.Down)]
                elif c == Mirrors.RightDown:
                    return [LightBeam(row, col, Direction.Right)]
                elif c == Mirrors.RightUp:
                    return [LightBeam(row, col, Direction.Left)]
                else:
                    return [LightBeam(row, col, Direction.Left), LightBeam(row, col, Direction.Right)]

            if light.direction == Direction.Left:
                if c == Mirrors.Horizontal:
                    return [LightBeam(row, col, Direction.Left)]
                elif c == Mirrors.RightDown:
                    return [LightBeam(row, col, Direction.Up)]
                elif c == Mirrors.RightUp:
                    return [LightBeam(row, col, Direction.Down)]
                else:
                    return [LightBeam(row, col, Direction.Up), LightBeam(row, col, Direction.Down)]

            if light.direction == Direction.Right:
                if c == Mirrors.Horizontal:
                    return [LightBeam(row, col, Direction.Right)]
                elif c == Mirrors.RightDown:
                    return [LightBeam(row, col, Direction.Down)]
                elif c == Mirrors.RightUp:
                    return [LightBeam(row, col, Direction.Up)]
                else:
                    return [LightBeam(row, col, Direction.Up), LightBeam(row, col, Direction.Down)]



        error(f"No correct mirror or direction {c} {light}")
        return ([])


    def light_move(self):
        steps = 0
        while len(self.lights) > 0:

            # debug(f"Step {steps}:\n{self.print_state()}")

            l = self.lights.pop()
            new_ls = self.move_light(l)
            for nl in new_ls:
                self.lights.append(nl)
            steps += 1


    def energized(self):
        return sum([sum([s[1] for s in row]) for row in self.matrix])


    def print_state(self):
        s = []
        for row in self.matrix:
            s.append([])
            for v in row:
                if v[0] == Mirrors.Non:
                    s[-1].append(".")
                elif v[0] == Mirrors.Horizontal:
                    s[-1].append("-")
                elif v[0] == Mirrors.Vertical:
                    s[-1].append("|")
                elif v[0] == Mirrors.RightDown:
                    s[-1].append("\\")
                elif v[0] == Mirrors.RightUp:
                    s[-1].append("/")

        for light in self.lights:
            if s[light.row][light.col] not in ".-|/\\":
                s[light.row][light.col] = "X"

            elif light.direction == Direction.Up:
                s[light.row][light.col] = "^"
            elif light.direction == Direction.Down:
                s[light.row][light.col] = "v"
            elif light.direction == Direction.Left:
                s[light.row][light.col] = "<"
            elif light.direction == Direction.Right:
                s[light.row][light.col] = ">"

        return '\n'.join([''.join(r) for r in s])


    def print_energized(self):
        s = ""
        for row in self.matrix:
            for v in row:
                if v[1]:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        return s


################################################################################
def solution_a(inp):
    b = Board(inp)
    b.light_move()
    debug(b.print_energized())
    return b.energized()

################################################################################

################################################################################
def solution_b(inp):
    max_value = 0
    r = len(inp)
    c = len(inp[0])
    steps = 0

    # From left
    debug("From the left")
    for i in range(r):
        b = Board(inp)
        b.lights = [LightBeam(i, -1, Direction.Right)]
        b.light_move()
        m = b.energized()
        if m > max_value:
            debug(f"New max found: {m} in step {steps}")
            max_value = m
        steps += 1

    # From right
    debug("From the right")
    for i in range(r):
        b = Board(inp)
        b.lights = [LightBeam(i, c, Direction.Left)]
        b.light_move()
        m = b.energized()
        if m > max_value:
            debug(f"New max found: {m} in step {steps}")
            max_value = m
        steps += 1

    # From up
    debug("From the top")
    for i in range(r):
        b = Board(inp)
        b.lights = [LightBeam(-1, i, Direction.Down)]
        b.light_move()
        m = b.energized()
        if m > max_value:
            debug(f"New max found: {m} in step {steps}")
            max_value = m
        steps += 1

    # From down
    debug("From the bottomjo")
    for i in range(r):
        b = Board(inp)
        b.lights = [LightBeam(r, i, Direction.Up)]
        b.light_move()
        m = b.energized()
        if m > max_value:
            debug(f"New max found: {m} in step {steps}")
            max_value = m
        steps += 1

    return max_value
