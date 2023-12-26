
# Load utils
import sys
sys.path.append('../../')
from utils import *

import re

################################################################################
def solution_a(inp):

    debug(f'Solution A with input: {inp}')

    total = 0

    for line in inp:

        # Remove all non-numeric characters
        line = re.sub(r"[^0-9]", "", line)

        # Get the first and last
        m = int(line[0] + line[-1])
        total += m

    return total


################################################################################
def solution_b(inp):

    n_dic = {
        # 0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine"
    }

    inp_2 = []

    for line in inp:

        # For each str digit, convert it to digit
        i = 0
        while i < len(line):
            for k, v in n_dic.items():
                if line[i:].startswith(v):
                    line = line[:i] + str(k) + line[i:]
                    i += 1
                    break
            i += 1

        inp_2.append(line)

    return solution_a(inp_2)
