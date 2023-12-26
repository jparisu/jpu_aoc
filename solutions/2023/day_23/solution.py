
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
transform_inp = {
    "." : 0,
    "#" : 1,
    "<" : 2,
    ">" : 3,
    "v" : 4,
    "^" : 5
}

transform_inp_b = {
    "." : 0,
    "#" : 1,
    "<" : 0,
    ">" : 0,
    "v" : 0,
    "^" : 0
}

class Direction(Enum):
    Up = 5
    Down = 4
    Left = 2
    Right = 3

class Board(GeneralBoard):

    def __init__(self, inp, transform=transform_inp):
        super().__init__(inp, transform=transform)

        # OriginX  OriginY  FinalX  FinalY  Length
        self.paths = []

        already_searched = set()
        to_search = {(0,1,Direction.Down)}

        while len(to_search) > 0:

            x, y, d = to_search.pop()
            if (x, y, d) in already_searched:
                continue

            already_searched.add((x, y, d))

            debug(f"Ready to searh path from {x},{y}  with dir {d.name}")

            res = self.create_path(x,y,d)

            if res == None:
                continue

            ox, oy, dirs = res

            debug(f"Found: {ox},{oy}  {dirs}")
            debug("")

            for d in dirs:
                to_search.add((ox, oy, d))


    def create_path(self, x, y, origin_dir: Direction):
        curr_x, curr_y = x, y

        if origin_dir == Direction.Down:
            curr_x += 1
        elif origin_dir == Direction.Up:
            curr_x -= 1
        elif origin_dir == Direction.Left:
            curr_y -= 1
        else:
            curr_y += 1

        last_dir = origin_dir
        length = 1

        while True:

            if curr_x == self.nr - 1 and curr_y == self.nc - 2:
                self.paths.append([x, y, curr_x, curr_y, length])
                return None

            neigs = []

            if (last_dir != Direction.Down
                    and self.matrix[curr_x-1][curr_y] != 1
                    and self.matrix[curr_x-1][curr_y] != 4):
                neigs.append((curr_x-1, curr_y, Direction.Up))

            if (last_dir != Direction.Up
                    and self.matrix[curr_x+1][curr_y] != 1
                    and self.matrix[curr_x+1][curr_y] != 5):
                neigs.append((curr_x+1, curr_y, Direction.Down))

            if (last_dir != Direction.Right
                    and self.matrix[curr_x][curr_y-1] != 1
                    and self.matrix[curr_x][curr_y-1] != 3):
                neigs.append((curr_x, curr_y-1, Direction.Left))

            if (last_dir != Direction.Left
                    and self.matrix[curr_x][curr_y+1] != 1
                    and self.matrix[curr_x][curr_y+1] != 2):
                neigs.append((curr_x, curr_y+1, Direction.Right))

            if len(neigs) == 1:
                curr_x, curr_y, last_dir = neigs[0]
                length += 1

            elif len(neigs) == 0:
                return None

            else:
                self.paths.append([x, y, curr_x, curr_y, length])
                return (curr_x, curr_y, [n[2] for n in neigs])


    def generate_graph(self) -> Graph:

        nodes = {f"[{self.nc-1}, {self.nr-2}]": {}}

        for ox, oy, fx, fy, leng in self.paths:
            ini = str([ox,oy])
            fin = str([fx,fy])
            if ini not in nodes.keys():
                nodes[ini] = {}
            if fin in nodes[ini].keys():
                nodes[ini][fin] = max(leng, nodes[ini][fin])
            else:
                nodes[ini][fin] = leng

        return Graph(nodes)

    def generate_non_slippery_graph(self) -> Graph:

        nodes = {f"[{self.nc-1}, {self.nr-2}]": {}}

        for ox, oy, fx, fy, leng in self.paths:
            ini = str([ox,oy])
            fin = str([fx,fy])

            # Add go edge
            if ini not in nodes.keys():
                nodes[ini] = {}
            if fin in nodes[ini].keys():
                nodes[ini][fin] = max(leng, nodes[ini][fin])
            else:
                nodes[ini][fin] = leng

            # Add return edge
            if fin not in nodes.keys():
                nodes[fin] = {}
            if ini in nodes[fin].keys():
                nodes[fin][ini] = max(leng, nodes[fin][ini])
            else:
                nodes[fin][ini] = leng


        return Graph(nodes)


################################################################################
def solution_a(inp):
    b = Board(inp)
    g = b.generate_graph()
    debug(g)
    all_p = g.all_paths("[0, 1]", f"[{b.nc-1}, {b.nr-2}]")
    debug(all_p)
    max_distance = 0
    for p in all_p:
        dist = g.path_length(p)
        debug(f"Path: {p}  with distance {dist}")
        max_distance = max(max_distance, dist)
    return max_distance


################################################################################

################################################################################
def solution_b(inp):
    b = Board(inp, transform=transform_inp_b)
    g = b.generate_non_slippery_graph()
    debug(g)
    all_p = g.all_paths("[0, 1]", f"[{b.nc-1}, {b.nr-2}]")
    debug(all_p)
    max_distance = 0
    for p in all_p:
        dist = g.path_length(p)
        debug(f"Path: {p}  with distance {dist}")
        max_distance = max(max_distance, dist)
    return max_distance
