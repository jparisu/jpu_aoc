
# Load utils
import sys
sys.path.append('../../')
from utils import *

import re

################################################################################
def solution_a(inp):

    max_n = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    colors = max_n.keys()

    def is_possible(play: dict[str, int]):

        for color, v in play.items():
            if v > max_n[color]:
                return False

        return True

    ids_sum = 0

    # read for each game
    for line in inp:

        debug(f'Line: <{line}>')

        # read each play in each game
        game = line.split(":")[-1].strip()
        game_id = int(line.split(":")[0].split(" ")[-1])
        possible = True

        for play in game.split(";"):

            debug(f'Play: <{play}>')

            colors = [s.strip() for s in play.split(",")]

            # construct dict
            play_d = {}

            for color in colors:

                debug(f'Color: <{color}>')

                n, c = [s.strip() for s in color.split(" ")]
                n = int(n)
                play_d[c] = n

            debug(f'Play dict: <{play_d}>')

            # Check if possible
            if not is_possible(play_d):

                debug(f'Not possible! {play_d}')

                possible = False
                break

            else:
                debug(f'Possible! {play_d}')


        # Add ids of possible games
        if possible:
            ids_sum += game_id

    return ids_sum


################################################################################
def solution_b(inp):

    powers_sum = 0

    # read for each game
    for line in inp:

        debug(f'Line: <{line}>')

        # read each play in each game
        game = line.split(":")[-1].strip()
        game_id = int(line.split(":")[0].split(" ")[-1])

        min_cubes = {
            "red": 0,
            "green": 0,
            "blue": 0
        }

        for play in game.split(";"):

            debug(f'Play: <{play}>')

            colors = [s.strip() for s in play.split(",")]

            for color in colors:

                debug(f'Color: <{color}>')

                n, c = [s.strip() for s in color.split(" ")]
                n = int(n)

                if n > min_cubes[c]:
                    min_cubes[c] = n

        # Get the multiplication of the min cubes
        powers = min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
        debug(f'Powers: <{powers}> for game <{game_id}>')
        powers_sum += powers

    return powers_sum
