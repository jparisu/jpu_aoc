
# Load utils
import sys
sys.path.append('../../')
from utils import *

import numpy as np

################################################################################
class Recta:

    def __init__(self, line: str):
        l1, l2 = line.split("@")

        self.x, self.y, self.z = [int(l.strip()) for l in l1.split(",")]
        self.vx, self.vy, self.vz = [int(l.strip()) for l in l2.split(",")]

    def intersect_xy(self, other: "Recta") -> Tuple[float, float]:

        a1 = [ - self.vy / self.vx, 1]
        a2 = [ - other.vy / other.vx, 1]

        b1 = self.x * a1[0] + self.y * a1[1]
        b2 = other.x * a2[0] + other.y * a2[1]

        a = [a1, a2]
        b = [b1, b2]

        # debug(f"Intersect {self}  {other}")
        # debug(f"a={a}  b={b}")

        try:
            return np.linalg.solve(a, b)
        except np.linalg.LinAlgError as err:
            return None, None

    def does_intersect_xy(self, other: "Recta", xmin: int, xmax: int) -> bool:
        x, y = self.intersect_xy(other)
        if x is None:
            return False
        debug(f"{self} / {other}   ->   {x},{y}")
        debug(f"{self.is_in_trajectory(x, y)}")
        debug(f"{other.is_in_trajectory(x, y)}")
        debug(f"{Recta.in_square(x, y, xmin, xmax)}")
        return self.is_in_trajectory(x, y) and other.is_in_trajectory(x, y) and Recta.in_square(x, y, xmin, xmax)

    def is_in_trajectory(self, x: int, y: int):
        if self.vx > 0:
            if x < self.x:
                return False
        else:
            if x > self.x:
                return False

        if self.vy  > 0:
            if y < self.y:
                return False
        else:
            if y > self.y:
                return False

        return True

    def in_square(x, y, xmin, xmax) -> bool:
        return (
            x >= xmin and x <= xmax and
            y >= xmin and y <= xmax
        )


    def __str__(self) -> str:
        return f"{{ {self.x},{self.y},{self.z}  :  {self.vx},{self.vy},{self.vz} }}"


################################################################################
def solution_a(inp):
    rectas = [Recta(line) for line in inp]

    xmin = 7
    xmax = 27

    xmin = 200000000000000
    xmax = 400000000000000

    count = 0
    for i in range(len(rectas)):
        for j in range(i+1, len(rectas)):
            if rectas[i].does_intersect_xy(rectas[j], xmin, xmax):
                count += 1
    return count


################################################################################

################################################################################
def solution_b(inp):
    return -1
