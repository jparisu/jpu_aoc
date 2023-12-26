# jparisu Advent of Code solutions


My own Advent of Code solutions repository

This repository hosts common tools to make [AoC](https://adventofcode.com/) implementations easier,
as the solutions to the problems that I solve.

- [jparisu Advent of Code solutions](#jparisu-advent-of-code-solutions)
  - [How to use it](#how-to-use-it)
    - [Arguments](#arguments)
  - [How to create a new solution](#how-to-create-a-new-solution)
    - [Solution file](#solution-file)
      - [Raw input](#raw-input)
    - [Utils](#utils)
      - [Debug](#debug)
  - [History](#history)
    - [2023](#2023)

## How to use it

In order to run it, run the `main.py` file from the root of the repository:

``` bash
python3 main.py
```

### Arguments

It can be selected the **year** and **day**,
the **first** or **second** part of the problem,
whether to use the **test** input or the **real** one,
and whether to run it in **debug** mode or not.

``` bash
usage: main.py [-h] [-d] [-a DAY] [-y YEAR] [-b] [-t]

Execute Advent of Code solution

options:
  -h, --help            show this help message and exit
  -d, --debug
  -a DAY, --day DAY
  -y YEAR, --year YEAR
  -b, --second
  -t, --test
```

## How to create a new solution

Create a folder with the following structure:

``` bash
- solutions
  - <year>
    - day_<x>
      - solution.py
      - inputs
        - input.in
        - test.in
```

- `solution.py` is the file where the solution must be implemented.
- `input.in` file with the real input.
- `test.in` file with the test input.
- `test2.in` (optional) file with the test input for the second problem.

It is useful to copy and paste `day_x` as template.

### Solution file

In `solution.py` file must be implemented:

``` python
def solution_a(inp: List[str]) -> int:
    # First solution

def solution_b(inp: List[str]) -> int:
    # Second solution
```

#### Raw input

If the input must be passed to the function in raw format (in a line without modification)
set the variable `RAW_INPUT = True` somewhere in the file.
This is useful when blank lines are relevant.

### Utils

In order to use `utlis.py` add the following:

``` python
import sys
sys.path.append('../../')
from utils import *
```

There are many utils functions implemented, as input parsing, matrix handling, math operations, etc.

#### Debug

Use functions `debug(st: str)`, `info(st: str)` and `error(st: str)` for debug proposes.


## History

### 2023

- To day `December 26` I have obtained 44/50 stars.
