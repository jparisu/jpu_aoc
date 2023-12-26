
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
def h(s, x=0): return (h(s[1:],(((x+ord(s[0]))*17)%256)) if len(s) > 0 else x)

################################################################################
def solution_a(inp):
    return sum([h(i) for i in inp[0].split(",")])

################################################################################

################################################################################
def solution_b(inp):

    N = 256

    boxes = [[] for _ in range(N)]

    for l in inp[0].split(","):

        if "=" in l:
            label = l.split("=")[0]
            action = "="
        else:
            label = l.split("-")[0]
            action = "-"
        hash = h(label)

        if action == "-":
            i = 0
            while i < len(boxes[hash]):
                if boxes[hash][i][0] == label:
                    boxes[hash].pop(i)
                else:
                    i += 1

        else:
            number = int(l.split("=")[-1])

            found = False
            for i in range(len(boxes[hash])):
                if boxes[hash][i][0] == label:
                    boxes[hash][i][1] = number
                    found = True

            if not found:
                boxes[hash].append([label, number])


    result = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            result += (i+1) * (j+1) * lens[1]

    return result
