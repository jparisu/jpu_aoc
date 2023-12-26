
import sys
import os
import logging

from datetime import date
from typing import List, Tuple, Set, Dict
from enum import Enum
import copy

###############
# DEBUG TOOLS #
###############

def initialize_debug(activated=False):
    """Initialize debug mode with default configuration"""
    if activated:
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

def activate_debug(status=True):
    """Activate or deactivate debug messages"""
    if status:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

def info(st):
    """Print info message"""
    logging.info(str(st) + "\n")

def debug(st):
    """Print debug message"""
    logging.debug(str(st) + "\n")

def error(st):
    """Print error message"""
    logging.error(str(st) + "\n")


#############
# SYS TOOLS #
#############

def file_exists(path):
    """Checks if a file exists"""
    return os.path.isfile(path)

def get_current_day():
    """Returns the current day"""
    return date.today().day

def get_current_year():
    """Returns the current year"""
    return date.today().year

###################
# INPUT TREATMENT #
###################

def convert_to_ints(input):
    """Converts a list of strings to a list of ints"""
    return [int(x) for x in input]

def convert_line_to_ints(line, separator=','):
    """Converts a line of strings to a list of ints"""
    return [int(x) for x in line.split(separator)]

class GeneralBoard:
    """
    This class helps to create a matrix from the string given.
    This is used for many of the problems that uses maps or matrix.
    """

    def __init__(self, inp, transform={}):
        self.matrix = []
        for line in inp:
            self.matrix.append([])
            for c in line:
                if c in transform.keys():
                    self.matrix[-1].append(transform[c])
                else:
                    self.matrix[-1].append(c)
        self.transform = transform
        self.retransform = invert_dict(transform)
        self.nr = len(self.matrix)
        self.nc = len(self.matrix[0])

    def get_neigs(self, r, c) -> List[Tuple[int, int]]:
        neigs = []
        if r > 0:
            neigs.append((r-1, c))
        if r < self.nr-1:
            neigs.append((r+1, c))
        if c > 0:
            neigs.append((r, c-1))
        if c < self.nc-1:
            neigs.append((r, c+1))
        return neigs

    def get_matrix_value(self, r, c):
        return self.matrix[r][c]

    def set_matrix_value(self, r, c, value):
        self.matrix[r][c] = value

    def __str__(self):
        st = ""
        for line in self.matrix:
            for c in line:
                v = c
                if c in self.retransform.keys():
                    v = self.retransform[c]
                st += v
            st += "\n"

        return st

###################
# TO STRING TOOLS #
###################

def vector_to_str(v, sep=' '):
    """Converts a vector to a string"""
    return sep.join([str(x) for x in v])

def matrix_to_str(m, sep='\n'):
    """Converts a matrix to a string"""
    # TODO make it with delimiters and spaces
    return sep.join([vector_to_str(x) for x in m])


################
# MATRIX TOOLS #
################

def turn_matrix(matrix):
    """Turns a matrix 90 degrees clockwise"""
    len_rows = len(matrix)
    len_cols = len(matrix[0])
    new_matrix = [[None for _ in range(len_rows)] for _ in range(len_cols)]

    for i in range(len_rows):
        for j in range(len_cols):
            new_matrix[j][len_rows - i - 1] = matrix[i][j]
    return new_matrix

def volt_matrix_horizontally(matrix):
    """Volt matrix horizontally"""
    len_rows = len(matrix)
    len_cols = len(matrix[0])
    new_matrix = [[None for _ in range(len_cols)] for _ in range(len_rows)]

    for i in range(len_rows):
        for j in range(len_cols):
            new_matrix[len_rows - i - 1][j] = matrix[i][j]
    return new_matrix

###############
# MATHS TOOLS #
###############

def manhattan_distance(x, y, x_goal, y_goal):
    """Computes the manhattan distance between two points"""
    return manhattan_distance_vector([x, y], [x_goal, y_goal])

def manhattan_distance_vector(point, goal):
    """Computes the manhattan distance between two points"""
    return sum([abs(point[i]-goal[i]) for i in range(len(point))])

def char_is_numeric(c):
    v = ord(c)
    return v >= ord('0') and v <= ord('9')


##############
# DICT TOOLS #
##############

def count_values_to_dict(l: List):
    d = {}
    for i in l:
        if i not in d.keys():
            d[i] = 0
        d[i] += 1
    return d

def invert_dict(d: Dict) -> Dict:
    result = {}
    for k, v in d.items():
        result[v] = k
    return result

###############
# GRAPH TOOLS #
###############

class Graph:
    def __init__(self, nodes: Dict[str, Dict[str, int]]):
        self.nodes = nodes

    def neigs(self, node: str) -> Dict[str, int]:
        return self.nodes[node]

    def distance(self, node_src: str, node_tgt) -> int:
        if node_tgt in self.nodes[node_src].keys():
            return self.nodes[node_src][node_tgt]
        else:
            return -1

    def __str__(self) -> str:
        st = ""
        for node, neigs in self.nodes.items():
            st += node + " ->\n"
            for n, l in neigs.items():
                st += f"  {n} : {l}\n"
        return st

    def optimal_path(self, origin, end) -> Tuple[int, List[str]]:
        t = {}
        q = [(origin, 0, [])]

        while len(q) > 0:
            current, l, p = q.pop()
            p = p + [current]

            if current == end:
                return l, p

            if current in t.keys():
                continue

            t[current] = (l, p)

            for neig, new_l in self.neigs(current).items():
                if neig not in t.keys():
                    q.append((neig, l + new_l, p))

            q.sort(key= lambda x: x[1] , reverse=True)

        error(f"Not found a path")
        return None

    def reverse_weight(self):
        for k, v in self.nodes.items():
            for kk in v.keys():
                v[kk] = 1 / v[kk]

    def path_length(self, path: List[str]):
        l = 0
        for i in range(len(path)-1):
            l += self.nodes[path[i]][path[i+1]]
        return l

    def all_paths(self,
                origin: str,
                end: str,
                visited: List[str] = [],
                visited_s: Set[str] = set()
            ) -> Set[List[str]]:

        if origin == end:
            return [visited + [origin]]
        res = []

        visited.append(origin)
        visited_s.add(origin)

        for neig, _ in self.neigs(origin).items():
            if neig not in visited_s:
                for p in self.all_paths(neig, end, list(visited), set(visited_s)):
                    res.append(p)

        return res
