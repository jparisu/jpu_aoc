
import argparse
import sys

import utils


def parse_arguments():
    """Parse arguments from command line"""
    parser = argparse.ArgumentParser(description='Execute Advent of Code solution')
    parser.add_argument("-d", "--debug", action='store_true')
    parser.add_argument("-a", "--day", type=int, default=None)
    parser.add_argument("-y", "--year", type=int, default=None)
    # parser.add_argument("-r", "--raw", action='store_true')
    parser.add_argument("-b", "--second", action='store_true')
    parser.add_argument("-t", "--test", action='store_true')
    return parser.parse_args()


RAW_INPUT_ = False

def get_day(day):
    """If day argument is given, returns it, otherwise returns current day"""
    if day:
        return day
    else:
        return utils.get_current_day()

def get_year(year):
    """If year argument is given, returns it, otherwise returns current year"""
    if year:
        return year
    else:
        return utils.get_current_year()

def get_path(year, day):
    """Returns path to the solution"""
    return f'solutions/{year}/day_{day}'


def load_input(path, test, second, raw=False):
    """
    Loads input from file.

    If test is True, loads test input, otherwise loads normal input.

    If raw is True, loads input as raw,
    otherwise loads input as list of strings and strip each.
    """

    if test:
        # In case it is the second, check if test2.in exists and use it
        if second and utils.file_exists(f'{path}/inputs/test2.in'):
            file_path = f'{path}/inputs/test2.in'
        else:
            file_path = f'{path}/inputs/test.in'
    else:
        file_path = f'{path}/inputs/input.in'

    with open(file_path, 'r') as file:
        if raw:
            utils.debug('Using RAW input')
            data = [d for d in file.readlines()]
        else:
            data = [d.strip() for d in file.readlines()]
        utils.debug(f'INPUT: {data}')
        return data


def load_metainfo(path):
    """Load whether the solution says it must have RAW_INPUT or not."""
    sys.path.append(path)

    # RAW_INPUT
    try:
        from solution import RAW_INPUT
        if RAW_INPUT:
            utils.debug(f'Using RAW from module {RAW_INPUT}')
            return True
    except ImportError:
        pass
    return False


def solution(path, input, first_test=True):
    """Execute the solution for the given test case."""

    sys.path.append(path)

    if first_test:
        from solution import solution_a as Solution

    else:
        from solution import solution_b as Solution

    utils.debug('--- PROCESSING SOLUTION ---')

    result = Solution(input)

    utils.debug('--- FINISH PROCESSING SOLUTION ---')

    return result


def main():


    # Parse arguments
    args = parse_arguments()
    # args.debug
    # args.day
    # args.year
    # args.raw
    # args.second
    # args.test


    # Initialize debug mode
    utils.initialize_debug(args.debug)

    utils.debug('===== START ADVENT OF CODE SOLUTION =====')

    # Get year and day
    year = get_year(args.year)
    day = get_day(args.day)
    path = get_path(year, day)

    second_str = 'second ' if args.second else ''
    test_str = 'test case ' if args.test else ''
    utils.info(f'Solving {second_str}{test_str}problem of day {day} of {year}')

    # Get input
    raw = load_metainfo(path)
    case_input = load_input(path, args.test, args.second, raw)
    result = solution(path, case_input, not args.second)

    utils.info(f'SOLUTION:\n {result}')

    utils.debug('===== FINISH ADVENT OF CODE SOLUTION =====')


if __name__ == '__main__':
    main()
