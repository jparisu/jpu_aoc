
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Coordinate:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, __value: object) -> bool:
        return (
            self.x == __value.x
            and self.y == __value.y
            and self.z == __value.z)

    def __str__(self) -> str:
        return f"[{self.x},{self.y},{self.z}]"

    def drop(self):
        self.z -= 1
        return self

    def undrop(self):
        self.z += 1
        return self


class Piece:

    def __init__(self, line: str = None, points: List[Coordinate] = None):
        if line is not None:
            ini, fin = line.split("~")
            ini = list(map(int, ini.split(",")))
            fin = list(map(int, fin.split(",")))

            self.points = set()
            for x in range(fin[0]-ini[0]+1):
                for y in range(fin[1]-ini[1]+1):
                    for z in range(fin[2]-ini[2]+1):
                        self.points.add(Coordinate(ini[0]+x, ini[1]+y, ini[2]+z))

        else:
            self.points = points

        self.min_z = 10000
        for p in self.points:
            self.min_z = min(p.z, self.min_z)

    def drop(self):
        new_points = set()
        while len(self.points) > 0:
            new_points.add(self.points.pop().drop())
        self.points = new_points
        self.min_z -= 1

    def undrop(self):
        new_points = set()
        while len(self.points) > 0:
            new_points.add(self.points.pop().undrop())
        self.points = new_points
        self.min_z += 1

    def crashes(self, other: "Piece") -> bool:
        return len(self.points.intersection(other.points)) > 0

    def __str__(self) -> str:
        return f"< {[str(x) for x in self.points]} >"

    def max(self):
        x = 0
        y = 0
        z = 0
        for p in self.points:
            x = max(p.x, x)
            y = max(p.y, y)
            z = max(p.z, z)
        return Coordinate(x, y, z)


class Tetris:

    def __init__(self, pieces: List[Piece], base: bool = False):
        self.pieces = pieces
        self.
        self.n = len(pieces)

        x = 0
        y = 0
        for p in self.pieces:
            r = p.max()
            x = max(r.x, x)
            y = max(r.y, y)

        if not base:
            self.pieces.append(Piece(f"0,0,0~{x},{y},0"))
        else:
            self.n -= 1

    def drop_(self):
        dropped = []
        for i in range(self.n):
            self.pieces[i].drop()
            crashes = False
            for j in range(self.n+1):
                if i == j:
                    continue
                if self.pieces[i].crashes(self.pieces[j]):
                    crashes = True
                    break
            if crashes:
                self.pieces[i].undrop()
            else:
                dropped.append(i)
        return dropped

    def drop(self):
        while len(self.drop_()) > 0: pass

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
            if len(t.drop_()) == 0:
                count += 1
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
    return -1
