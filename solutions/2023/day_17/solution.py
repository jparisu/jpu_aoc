
# Load utils
import sys
sys.path.append('../../')
from utils import *

from enum import Enum

################################################################################
class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class Info:
    def __init__(self, row: int, col: int, value: int, direction: Direction, direction_n: int):
        self.row = row
        self.col = col
        self.value = value
        self.direction = direction
        self.direction_n = direction_n

    def __lt__(self, other: "Info") -> bool:
        if self.row < other.row:
            return True
        elif self.row > other.row:
            return False
        elif self.col < other.col:
            return True
        elif self.col > other.col:
            return False
        elif self.direction.value < other.direction.value:
            return True
        elif self.direction.value > other.direction.value:
            return False
        elif self.direction_n < other.direction_n:
            return True
        elif self.direction_n > other.direction_n:
            return False
        return False

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: "Info") -> bool:
        return (
            self.row == other.row
            and self.col == other.col
            and self.direction.value == other.direction.value
            and self.direction_n == other.direction_n
        )

    def __str__(self) -> str:
        return f"[{self.row},{self.col}]({self.direction}-{self.direction_n})"


class Board:
    def __init__(self, lines: List[str]):
        self.matrix = [[int(c) for c in line] for line in lines]
        self.nr = len(self.matrix)
        self.nc = len(self.matrix[0])

    def value(self, row: int, col: int):
        return self.matrix[row][col]


class Node:
    def __init__(self, info: Info, board: Board):
        self.info = info
        self.board = board

    def __lt__(self, other: "Node") -> bool:
        return self.info < other.info

    def __eq__(self, other: "Node") -> bool:
        return self.info == other.info

    def __hash__(self) -> int:
        return hash(self.info)

    def neigs(self) -> List["Node"]:
        res = []

        if self.info.row > 0 and (self.info.direction_n < 3 or self.info.direction != Direction.Up) and self.info.direction != Direction.Down:
            res.append(self.generate_neig(Direction.Up))

        if self.info.row < self.board.nr - 1 and (self.info.direction_n < 3 or self.info.direction != Direction.Down) and self.info.direction != Direction.Up:
            res.append(self.generate_neig(Direction.Down))

        if self.info.col > 0 and (self.info.direction_n < 3 or self.info.direction != Direction.Left) and self.info.direction != Direction.Right:
            res.append(self.generate_neig(Direction.Left))

        if self.info.col < self.board.nc - 1 and (self.info.direction_n < 3 or self.info.direction != Direction.Right) and self.info.direction != Direction.Left:
            res.append(self.generate_neig(Direction.Right))

        return res

    def generate_neig(self, direction) -> "Node":

        info = Info(self.info.row, self.info.col, 0, direction, 1)

        if direction == Direction.Up:
            info.row -= 1
        elif direction == Direction.Down:
            info.row += 1
        elif direction == Direction.Left:
            info.col -= 1
        elif direction == Direction.Right:
            info.col += 1

        if direction == self.info.direction:
            info.direction_n += self.info.direction_n

        info.value = self.board.value(info.row, info.col)

        return Node(info, self.board)

    def __str__(self) -> str:
        return str(self.info)


def h(node: Node) -> int:
    return (node.board.nr - node.info.row - 1) + (node.board.nc - node.info.col - 1)


class Astar_element:
    def __init__(self, node: Node, g: int = 0, path: List[Node] = []) -> None:
        self.node = node
        self.path = path
        self.g = g
        self.h = h(node)
        self.f = self.g + self.h

    def __lt__(self, other: "Astar_element"):
        return self.f < other.f

    def extend_path(self) -> List[Node]:
        return self.path + [self.node]


def a_star(board: Board, start: Node, max_steps: int = 10000000) -> Tuple[List[Node], int]:

    steps = 0
    terminated = {}
    q = [Astar_element(start)]

    while len(q) > 0 and max_steps > steps:
        current = q.pop()
        steps += 1

        if current.node in terminated.keys():
            continue

        if steps % 1000 == 0:
            debug(f"Visiting Node: {current.node} with g: {current.g} and f: {current.f} in step {steps}")

        # If it is terminated
        if current.h == 0:
            return current.extend_path(), current.g

        terminated[current.node] = current

        for n in current.node.neigs():
            if n not in terminated.keys():
                q.append(Astar_element(n, current.g + n.info.value, current.extend_path()))

        q.sort(reverse=True)

    error(f"Has terminated without taking {max_steps} steps")


################################################################################
def solution_a(inp):
    b = Board(inp)
    start_node = Node(Info(0, 0, 2, Direction.Up, 0), b)
    final_node, distance = a_star(b, start_node)
    return distance

################################################################################


class Node2(Node):
    def neigs(self) -> List["Node2"]:
        res = []

        n = self.generate_up()
        if n is not None:
            res.append(n)

        n = self.generate_down()
        if n is not None:
            res.append(n)

        n = self.generate_left()
        if n is not None:
            res.append(n)

        n = self.generate_right()
        if n is not None:
            res.append(n)

        return res


    def generate_up(self) -> "Node2":

        if self.info.direction == Direction.Up:
            if self.info.direction_n < 10 and self.info.row > 0:
                value = self.board.value(self.info.row-1, self.info.col)
                return Node2(Info(self.info.row - 1, self.info.col, value, Direction.Up, self.info.direction_n + 1), self.board)

        elif self.info.direction != Direction.Down:
            if self.info.row >= 4:
                value = 0
                for i in range(4):
                    value += self.board.value(self.info.row - i - 1, self.info.col)
                return Node2(Info(self.info.row - 4, self.info.col, value, Direction.Up, 4), self.board)

        return None


    def generate_down(self) -> "Node2":

        if self.info.direction == Direction.Down:
            if self.info.direction_n < 10 and self.info.row < self.board.nr - 1:
                value = self.board.value(self.info.row+1, self.info.col)
                return Node2(Info(self.info.row + 1, self.info.col, value, Direction.Down, self.info.direction_n + 1), self.board)

        elif self.info.direction != Direction.Up:
            if self.info.row <= self.board.nr - 5:
                value = 0
                for i in range(4):
                    value += self.board.value(self.info.row + i + 1, self.info.col)
                return Node2(Info(self.info.row + 4, self.info.col, value, Direction.Down, 4), self.board)

        return None


    def generate_left(self) -> "Node2":

        if self.info.direction == Direction.Left:
            if self.info.direction_n < 10 and self.info.col > 0:
                value = self.board.value(self.info.row, self.info.col-1)
                return Node2(Info(self.info.row, self.info.col-1, value, Direction.Left, self.info.direction_n + 1), self.board)

        elif self.info.direction != Direction.Right:
            if self.info.col >= 4:
                value = 0
                for i in range(4):
                    value += self.board.value(self.info.row, self.info.col - i - 1)
                return Node2(Info(self.info.row, self.info.col - 4, value, Direction.Left, 4), self.board)

        return None


    def generate_right(self) -> "Node2":

        if self.info.direction == Direction.Right:
            if self.info.direction_n < 10 and self.info.col < self.board.nc - 1:
                value = self.board.value(self.info.row, self.info.col+1)
                return Node2(Info(self.info.row, self.info.col+1, value, Direction.Right, self.info.direction_n + 1), self.board)

        elif self.info.direction != Direction.Left:
            if self.info.col <= self.board.nc - 5:
                value = 0
                for i in range(4):
                    value += self.board.value(self.info.row, self.info.col + i + 1)
                return Node2(Info(self.info.row, self.info.col + 4, value, Direction.Right, 4), self.board)

        return None



################################################################################
def solution_b(inp):
    b = Board(inp)
    start_node = Node2(Info(0, 0, 2, Direction.Up, 0), b)
    path_nodes, distance = a_star(b, start_node)
    for p in path_nodes:
        debug(f"{p}")
    return distance
