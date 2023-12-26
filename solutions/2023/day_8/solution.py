
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
def solution_a(inp):

    instructions = inp[0]

    paths = {}
    for l in inp[1:]:
        paths[l[0:3]] = { "L" : l[7:10] , "R" : l[12:15] }

    node = "AAA"
    i = 0
    steps = 0
    while node != "ZZZ":
        node = paths[node][instructions[i]]
        steps += 1
        i = steps % len(instructions)

    return steps


################################################################################
def solution_b_(inp):

    instructions = inp[0]

    paths = {}
    for l in inp[2:]:
        paths[l[0:3]] = { "L" : l[7:10] , "R" : l[12:15] }

    nodes = []
    for n in paths.keys():
        if n[2] == "A":
            nodes.append(n)

    def all_end_in_z(nodes):
        for n in nodes:
            if n[2] != "Z":
                return False
        return True

    def move_nodes(nodes, instruction):
        res = []
        for n in nodes:
            res.append(paths[n][instruction])
        return res

    i = 0
    steps = 0
    while not all_end_in_z(nodes):
        nodes = move_nodes(nodes, instructions[i])
        steps += 1
        i = steps % len(instructions)
        if steps % 10000 == 0:
            debug(f"Working in step {steps}")

    return steps


################################################################################
def next_node(paths, node, instruction):
    return paths[node][instruction]


def full_path(paths, node, instructions):
    visited = set()
    current_node = node
    current_i = 0
    visited_list = []

    while (current_node, current_i) not in visited:
        visited.add((current_node, current_i))
        visited_list.append((current_node, current_i))

        current_node = next_node(paths, current_node, instructions[current_i])
        current_i += 1
        current_i %= len(instructions)

    # calculate the loop size
    loop_size = 0
    for i, v in enumerate(visited_list):
        if v == (current_node, current_i):
            loop_size = len(visited_list) - i

    real_visited = [v[0] for v in visited_list]

    return real_visited, loop_size


def indexes_of_z(nodes):
    res = []
    for i, n in enumerate(nodes):
        if n[2] == "Z":
            res.append(i)
    return res


def path_n(paths, node, instructions, n):
    for i in range(n):
        node = next_node(paths, node, instructions[i%len(instructions)])
    return node


def mcd(a, b):
    if b == 0:
        return a
    else:
        return mcd(b, a%b)


def mcm(a, b):
    return a*b//mcd(a, b)


def solution_b(inp):

    instructions = inp[0]

    paths = {}
    for l in inp[2:]:
        paths[l[0:3]] = { "L" : l[7:10] , "R" : l[12:15] }

    a_nodes = []
    for n in paths.keys():
        if n[2] == "A":
            a_nodes.append(n)
    debug(f"A nodes: {len(a_nodes)}")

    res = []
    loop_sizes = []
    for a in a_nodes:
        f, loop = full_path(paths, a, instructions)
        zs = indexes_of_z(f)
        res.append((len(f), loop))
        debug(f"{a}  {len(f)}  {loop}  {zs}")
        loop_sizes.append(loop)

    # node1 = "11A"
    # node2 = "22A"
    # node3 = "33A"
    # for i in range(1, 7):
    #     debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    #     debug(f"Node: {node2}  after {i} steps  {path_n(paths, node2, instructions, i)}")
    #     debug(f"Node: {node3}  after {i} steps  {path_n(paths, node3, instructions, i)}")
    #     debug("")

    node1 = "QXA"
    i = 0
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 1
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 2
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 3
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 12642
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 12643
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 12644
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 12645
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 12646
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")

    i = 12643*2
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")

    i = 12643*3
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")

    node1 = "PDA"
    i = 14257*1
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 14257*2
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")
    i = 14257*3
    debug(f"Node: {node1}  after {i} steps  {path_n(paths, node1, instructions, i)}")


    m = 1
    for l in loop_sizes:
        m = mcm(m, l)

    return m


"""
882250000 too low

('QXA', 12645, [12643], 12643)

('PDA', 14261, [14257], 14257)

('TDA', 15873, [15871], 15871)

('QQA', 18027, [18023], 18023)

('PPA', 19642, [19637], 19637)

('AAA', 16411, [16409], 16409)
"""
