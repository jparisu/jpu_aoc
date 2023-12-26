
# Load utils
import sys
sys.path.append('../../')
from utils import *

RAW_INPUT = True
import math
from typing import List
from copy import deepcopy

################################################################################

class Map:

    def __init__(self, lines):
        debug(lines)
        self.source = ""
        self.destination = ""
        self.ranges = []
        self.get_source_destination(lines[0])
        self.get_ranges(lines[1:])

    def get_source_destination(self, line):
        s, _, d = line.split()[0].split("-")
        self.source = s
        self.destination = d

    def get_ranges(self, lines):
        for l in lines:
            self.ranges.append(list(map(int, l.split())))

    def get_destination(self, value):
        for f in self.ranges:
            if Map.is_in_range(value, f):
                return f[0] + value - f[1]
        return value

    def is_in_range(value, range):
        return value >= range[1] and value - range[1] < range[2]

    def __str__(self):
        return f"{self.source}  {self.destination}\n {self.ranges}"






def solution_a(inp):

    seeds = list(map(int, inp[0].split(":")[1].split()))
    maps = []

    map_lines = []
    for l in inp[2:]:
        l = l.strip()
        if l == "":
            maps.append(Map(map_lines))
            map_lines = []
        else:
            map_lines.append(l)

    maps.append(Map(map_lines))

    debug('\n'.join([str(m) for m in maps]))

    for m in maps:
        new_seeds = []
        for s in seeds:
            new_seeds.append(m.get_destination(s))
        seeds = new_seeds

    return min(seeds)

################################################################################

class Range:

    def __init__(self, ini, end):
        self.ini = ini
        self.end = end

    def __lt__(self, other: "Range") -> bool:
        if self.ini == other.ini:
            return self.end < other.end
        else:
            return self.ini < other.ini

    def __eq__(self, __value: "Range") -> bool:
        return self.ini == __value.ini and self.end == __value.end

    def __str__(self) -> str:
        return f"< {self.ini} : {self.end} >"

    def joinable(self, other: "Range") -> bool:
        return (
            (self.ini >= other.ini and self.ini <= other.end)
            or
            (self.end >= other.ini and self.end <= other.end)
            or
            (self.end == other.ini - 1)
            or
            (self.ini == other.end + 1)
            or
            (self.ini <= other.ini and self.end >= other.end)
            or
            (other.ini <= self.ini and other.end >= self.end)
        )

    def join_2_ranges(x: "Range", y: "Range", joinable: bool = None) -> List["Range"]:
        if joinable is None:
            joinable = x.joinable(y)
        if joinable:
            return [Range(min(x.ini, y.ini), max(x.end, y.end))]
        else:
            return [x, y]

    def join(ranges: List["Range"]) -> List["Range"]:
        ranges.sort()
        result = [ranges[0]]

        for r in ranges[1:]:
            res = Range.join_2_ranges(result[-1], r)
            if len(res) == 1:
                result[-1] = res[0]
            else:
                result.append(res[1])

        return result

    def cut(x: "Range", c: int) -> List["Range"]:
        if x.ini >= c or x.end <= c:
            return [x]
        else:
            return [
                Range(x.ini, c),
                Range(c, x.end)]

    def included(self, other: "Range") -> bool:
        mi = min(self, other)
        mx = max(self, other)

        return (not (mi.end < mx.ini or not mi.end >= mx.end)) or (mi.ini == mx.ini)



class Map:

    def __init__(self, lines):
        debug(lines)
        self.source = ""
        self.destination = ""
        self.ranges = []
        self.cuts = []
        self.get_source_destination(lines[0])
        self.get_ranges(lines[1:])

    def get_source_destination(self, line):
        s, _, d = line.split()[0].split("-")
        self.source = s
        self.destination = d

    def get_ranges(self, lines):
        for l in lines:
            x, y, z = map(int, l.split())
            self.ranges.append([Range(y, y+z), x-y])
            self.cuts.append(y)
            self.cuts.append(y+z)

    def get_destination(self, value):
        for f in self.ranges:
            if Map.is_in_range(value, f):
                return f[0] + value - f[1]
        return value

    def is_in_range(value, range):
        return value >= range[1] and value - range[1] < range[2]

    def __str__(self):
        ranges = '\n '.join([f"{r} - {v}" for r, v in self.ranges])
        return f"{self.source}  {self.destination}\n {ranges}"

    def get_new_ranges(self, ranges: List[Range]) -> List[Range]:
        rs = []

        for r in ranges:
            rans = [r]
            for c in self.cuts:
                new_rans = []
                while len(rans) > 0:
                    i = rans.pop()
                    new_rans += Range.cut(i, c)

                rans = new_rans
            rs += rans



        # for c in self.cuts:
        #     cutted = False
        #     for r in ranges:
        #         res = Range.cut(r, c)
        #         if len(res) > 1:
        #             cutted = True
        #         rs += res

        debug(f"rs:  {'  '.join([str(x) for x in rs])}")

        result = []
        for r in rs:
            added = False
            for f, v in self.ranges:
                if r.included(f):
                    added = True
                    result.append(Range(r.ini + v, r.end + v))
                    # debug(f"r {r}  with f {f} is added as {result[-1]}")
                    break

            if not added:
                result.append(r)
                # debug(f"r {r}   is added as {result[-1]}")

        return Range.join(result)


def solution_b(inp):

    seeds_ranges = list(map(int, inp[0].split(":")[1].split()))
    seeds = []

    for i in range(0, len(seeds_ranges), 2):
        seeds.append(Range(seeds_ranges[i], seeds_ranges[i]+seeds_ranges[i+1]))

    seeds = Range.join(seeds)

    maps = []

    map_lines = []
    for l in inp[2:]:
        l = l.strip()
        if l == "":
            maps.append(Map(map_lines))
            map_lines = []
        else:
            map_lines.append(l)

    maps.append(Map(map_lines))

    debug('\n\n'.join([str(m) for m in maps]))

    debug(sum([seeds_ranges[i] for i in range(len(seeds_ranges)) if i%2==1]))
    min_v = math.inf

    debug('   '.join([str(x) for x in seeds]))

    for m in maps:
        s = deepcopy(seeds)
        seeds = m.get_new_ranges(seeds)
        debug(f"\n\n{m} :\n\n  {'   '.join([str(x) for x in s])}\n  {'   '.join([str(x) for x in seeds])}")

    return seeds[0].ini
