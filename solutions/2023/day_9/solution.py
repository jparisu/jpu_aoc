
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
def is_zeros(n):
    for i in n:
        if i != 0:
            return False
    return True

def next_iteration(n):
    res = []
    for i in range(len(n)-1):
        res.append(n[i+1] - n[i])
    return res

def extrapolate(n):
    res = 0
    if not is_zeros(n):
        next = next_iteration(n)
        r = extrapolate(next)
        res = r + n[-1]

    debug(f"Extrapolate: {n} -> {res}")
    return res

################################################################################
def solution_a(inp):
    result = 0
    for line in inp:
        ns = list(map(int, line.split()))
        e = extrapolate(ns)
        result += e

        debug(f"Extrapolate {ns} -> {e}")

    return result

################################################################################
def disextrapolate(n):
    res = 0
    if not is_zeros(n):
        next = next_iteration(n)
        r = disextrapolate(next)
        res = n[0] - r

    debug(f"Diextrapolate: {n} -> {res}")
    return res

################################################################################
def solution_b(inp):
    result = 0
    for line in inp:
        ns = list(map(int, line.split()))
        e = disextrapolate(ns)fire
        result += e

    return result
