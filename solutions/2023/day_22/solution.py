
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Piece:

    def __init__(self, line: str = None, other: "Piece" = None):
        if line is not None:
            ini, fin = line.split("~")
            self.min_x, self.min_y, self.min_z = map(int, ini.split(","))
            self.max_x, self.max_y, self.max_z = map(int, fin .split(","))

        else:
            self.min_x = other.min_x
            self.min_y = other.min_y
            self.min_z = other.min_z
            self.max_x = other.max_x
            self.max_y = other.max_y
            self.max_z = other.max_z

    def drop(self):
        self.min_z -= 1
        self.max_z -= 1

    def undrop(self):
        self.min_z += 1
        self.max_z += 1

    def crashes_when_drop(self, other: "Piece") -> bool:
        if self.min_z - 1 == other.max_z:
            return Piece.area_touches(
                self.min_x, self.max_x, self.min_y, self.max_y,
                other.min_x, other.max_x, other.min_y, other.max_y)
        return False

    def __str__(self) -> str:
        return f"< [{self.min_x},{self.max_x}] , [{self.min_y},{self.max_y}] , [{self.min_z},{self.max_z}] >"

    def area_touches(x0_min, x0_max, y0_min, y0_max, x1_min, x1_max, y1_min, y1_max):
        if x0_max < x1_min:
            return False
        elif x1_max < x0_min:
            return False
        elif y0_max < y1_min:
            return False
        elif y1_max < y0_min:
            return False
        return True

    def max(self):
        return self.max_x, self.max_y, self.max_z


class Tetris:

    def __init__(self, pieces: List[Piece], already_base: bool = False):
        self.pieces = pieces
        self.n = len(pieces)

        if not already_base:
            x = 0
            y = 0
            for p in self.pieces:
                xm, ym, _ = p.max()
                x = max(xm, x)
                y = max(ym, y)
            self.pieces.append(Piece(f"0,0,0~{x},{y},0"))

        else:
            self.n -= 1

        self.floor = [False for _ in range(len(self.pieces))]
        self.floor[-1] = True
        self.dropped = [False for _ in range(len(self.pieces))]


    def drop_(self) -> int:
        dropped = 0
        for i in range(self.n):
            if not self.floor[i]:
                crashes = -1
                for j in range(self.n+1):
                    if i == j:
                        continue
                    if self.pieces[i].crashes_when_drop(self.pieces[j]):
                        crashes = j
                        break
                if crashes == -1:
                    self.pieces[i].drop()
                    self.dropped[i] = True
                    dropped += 1
                else:
                    if self.floor[j]:
                        self.floor[i] = True
        return dropped

    def drop(self) -> int:
        dropped = 0
        d = self.drop_()
        while d > 0:
            dropped += d
            d = self.drop_()
        return sum([1 for x in self.dropped if x])

    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self.pieces])

    def how_many_drop(self) -> int:
        count = 0
        for i in range(self.n):
            pieces = []
            for j in range(self.n + 1):
                if i != j:
                    pieces.append(copy.deepcopy(self.pieces[j]))
            t = Tetris(pieces, True)
            if not t.drop_():
                debug(f"Removing piece {i} {self.pieces[i]} do not drop")
                count += 1
            else:
                debug(f"Removing piece {i} {self.pieces[i]} DO drop")
        return count

    def how_many_disintegrate(self) -> int:
        count = 0
        for i in range(self.n):
            pieces = []
            for j in range(self.n + 1):
                if i != j:
                    pieces.append(copy.deepcopy(self.pieces[j]))
            t = Tetris(pieces, True)
            v = t.drop()
            count += v
            debug(f"Removing piece {i} {self.pieces[i]} drop {v} pieces")
        return count


################################################################################
def solution_a(inp):
    t = Tetris([Piece(line) for line in inp])
    debug(t)
    t.drop()
    debug(t)
    return t.how_many_drop()


################################################################################

################################################################################
def solution_b(inp):
    t = Tetris([Piece(line) for line in inp])
    debug("Tetris generated")
    t.drop()
    debug("Tetris dropped")
    return t.how_many_disintegrate()
