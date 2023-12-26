
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Race:

    def __init__(self, time: int, distance: int):
        self.time = time
        self.distance = distance

    def calculate_ways_to_win(self):
        ways = 0
        for time_hold in range(1,self.time):
            distance = time_hold * (self.time - time_hold)
            if distance > self.distance:
                ways += 1
        return ways

    def calculate_ways_to_win_optimally(self):

        r1, r2 = map(int,grade_2_polynom(1, -self.time, self.distance))

        return r2 - r1


def solution_a(inp):

    times = list(map(lambda x: int(x.strip()), inp[0].split(":")[-1].split()))
    dists = list(map(lambda x: int(x.strip()), inp[1].split(":")[-1].split()))

    races = [Race(times[i], dists[i]) for i in range(len(times))]

    result = 1
    for r in races:
        result *= r.calculate_ways_to_win()

    return result

################################################################################
import math
def grade_2_polynom(a, b, c):
    s = math.sqrt(b*b - 4*a*c)

    r1 = (- b - s) / (2 * a)
    r2 = (- b + s) / (2 * a)

    return (r1, r2)


def solution_b(inp):

    time = int(''.join([x.strip() for x in inp[0].split(":")[-1].split()]))
    dist = int(''.join([x.strip() for x in inp[1].split(":")[-1].split()]))

    return Race(time, dist).calculate_ways_to_win_optimally()
