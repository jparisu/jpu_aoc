
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
def get_points(galaxy: List[List[str]]) -> Set[Tuple[int, int]]:
    res = set()
    for i in range(len(galaxy)):
        for j in range(len(galaxy[i])):
            if galaxy[i][j] == "#":
                res.add((i, j))
    return res

def expand(galaxy: List[List[str]], n=2) -> List[List[str]]:
    e_rows = empty_rows(galaxy)
    e_cols = empty_cols(galaxy)

    n_rows = len(galaxy) + len(e_rows) * (n-1)
    n_cols = len(galaxy[0]) + len(e_cols) * (n-1)

    res = [["." for _ in range(n_cols)] for _ in range(n_rows)]

    i_src = 0
    j_src = 0
    i = 0
    j = 0

    while i < n_rows:

        j = 0
        j_src = 0

        while j < n_cols:

            res[i][j] = galaxy[i_src][j_src]

            j_src += 1
            j += 1
            if j_src in e_cols:
                j += n-1

        i_src += 1
        i += 1
        if i_src in e_rows:
            i += n-1

    return res


def empty_rows(galaxy: List[List[str]]) -> Set[int]:
    res = set()
    for r in range(len(galaxy)):
        if row_is_empty(galaxy, r):
            res.add(r)
    return res

def empty_cols(galaxy: List[List[str]]) -> Set[int]:
    res = set()
    for c in range(len(galaxy[0])):
        if col_is_empty(galaxy, c):
            res.add(c)
    return res

def row_is_empty(galaxy: List[List[str]], row: int) -> bool:
    for c in galaxy[row]:
        if c == "#":
            return False
    return True

def col_is_empty(galaxy: List[List[str]], col: int) -> bool:
    for i in range(len(galaxy)):
        if galaxy[i][col] == "#":
            return False
    return True

def galaxy_to_str(galaxy: List[List[str]]) -> str:
    return '\n'.join([''.join(g) for g in galaxy])


def sum_manhattans(points: Set[Tuple[int, int]]):
    res = 0
    points = list(points)

    for i in range(len(points)):
        for j in range(i+1, len(points)):
            res += manhattan_distance_vector(points[i], points[j])

    return res


################################################################################
def solution_a(inp):
    inp = [list(i) for i in inp]
    galaxy = expand(inp)
    debug(galaxy_to_str(galaxy))
    points = get_points(galaxy)

    return sum_manhattans(points)

################################################################################
def expand_points(galaxy: List[List[str]], n: int) -> Set[Tuple[int, int]]:
    points = get_points(galaxy)
    e_rows = empty_rows(galaxy)
    e_cols = empty_cols(galaxy)

    res_points = set()

    for p in points:

        # rows before p
        row_before = 0
        for r in e_rows:
            if r < p[0]:
                row_before += 1

        col_before = 0
        for c in e_cols:
            if c < p[1]:
                col_before += 1

        res_points.add((p[0] + row_before * (n-1), p[1] + col_before * (n-1)))

    return res_points


################################################################################
def solution_b(inp):
    galaxy = [list(i) for i in inp]
    points = get_points(galaxy)
    N = 1000000
    points = expand_points(galaxy, N)
    debug(f"Points of galaxies with n {N} :  {sorted(points)}")
    return sum_manhattans(points)



"""
82000210
too low
"""
