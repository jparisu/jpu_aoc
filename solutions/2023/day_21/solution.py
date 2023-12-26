
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Board(GeneralBoard):

    def __init__(self, inp):
        super().__init__(inp, {".": 0, "S": 1, "#": -1})

    def step(self, n_step) -> None:
        for i in range(self.nr):
            for j in range(self.nc):
                v = self.get_matrix_value(i, j)
                if v == n_step:
                    neigs = self.get_neigs(i, j)
                    for ii, jj in neigs:
                        vv = self.get_matrix_value(ii, jj)
                        if vv != -1:
                            self.set_matrix_value(ii, jj, n_step+1)

    def count(self, n_step) -> int:
        res = 0
        for line in self.matrix:
            for v in line:
                if v == n_step:
                    res += 1
        return res


################################################################################
def solution_a(inp):
    N = 64
    b = Board(inp)
    for i in range(N):
        b.step(i+1)
    return b.count(N+1)

################################################################################

################################################################################
def solution_b(inp):
    return -1
