
# Load utils
import sys
sys.path.append('../../')
from utils import *

import re

################################################################################

# Number: line, start, length

def is_special_char(c):
    return not (char_is_numeric(c) or c == '.')


def find_numbers(matrix):
    res = []
    for l in range(len(matrix)):
        res += find_numbers_line(matrix, l)
    return res


def find_numbers_line(matrix, line):
    res = []
    index = 0
    while index < len(matrix[line]):

        start, length = find_number_in_line(matrix, line, index)

        if length <= 0:
            break
        else:
            res.append([line, start, length])
            index = start + length

    return res


def find_number_in_line(matrix, line, starting=0):
    start = -1
    in_num = False
    # debug(f"THE MATRIX: {matrix}")
    # debug(f"THE LINE: {matrix[line]}")
    for i, c in enumerate(matrix[line][starting:]):
        if char_is_numeric(c):
            if start == -1:
                start = i + starting
        else:
            if start != -1:
                return start, i + starting - start

    if start != -1:
        return start, len(matrix[line]) - start

    else:
        return -1, -1



def read_number(matrix, line, start, length):
    return int(matrix[line][start:start+length])


def get_indexes_touching(matrix, line, start, length):
    indexes = []
    for l in range(line-1, line+2):

        if l < 0 or l >= len(matrix):
            continue

        for i in range(start-1, start+length+1):

            if i < 0 or i >= len(matrix[0]):
                continue

            else:
                indexes.append([l, i])

    debug(f"Indexes for {line} {start} {length} are {indexes}")

    return indexes


def touches_char(matrix, line, start, length):
    for l, i in get_indexes_touching(matrix, line, start, length):
        if is_special_char(matrix[l][i]):
            return True
    return False


def check_number_value(matrix, line, start, length):
    if touches_char(matrix, line, start, length):
        debug(f"Number {matrix[line][start:start+length]} touches")
        return read_number(matrix, line, start, length)
    else:
        return 0


def solution_a(inp):
    return sum(
        [
            check_number_value(inp, line, start, length)
            for
            line, start, length
            in
            find_numbers(inp)
        ]
    )

"""
541416
too high

536667
too low
"""


################################################################################

def get_gear_indexes(matrix):
    indexes = []
    for l, line in enumerate(matrix):
        for i, c in enumerate(line):
            if c == "*":
                indexes.append([l, i])
    return indexes


def gear_value(matrix, g_line, g_index, numbers):
    touching = []
    gear = [g_line, g_index]
    for line, start, length in numbers:
        touching_indexes = get_indexes_touching(matrix, line, start, length)
        if gear in touching_indexes:
            touching.append([line, start, length])

    if len(touching) == 2:
        return (
            read_number(matrix, touching[0][0], touching[0][1], touching[0][2])
                *
            read_number(matrix, touching[1][0], touching[1][1], touching[1][2])
        )

    else:
        return 0


def gears_value(matrix, gears, numbers):
    s = 0
    for g in gears:
        s += gear_value(matrix, g[0], g[1], numbers)
    return s


def solution_b(inp):
    gears = get_gear_indexes(inp)
    numbers = find_numbers(inp)
    return gears_value(inp, gears, numbers)
