import re
from dataclasses import dataclass

TEST = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

"""
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#..^...v#    
.>>>>>^.#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#.
prev_grid   new_grid   prev_dir new_dir
1           2           up      down

1           3           left    down
1           6           right   left

2           1           up      down
3           1           up      right
2           6           left    up
4           6           right   down

2           5           down    up
3           5           down    right

6           4           up      left

5           3           left    up
6           1           right   left

5           2           down    up
6           2           down    right


  ####
  ####
  ##
  ##
####
####
##
##

prev_grid   new_grid   prev_dir new_dir
1           6           up      right
2           6           up      up

1           4           left    right
2           5           right   left

2           3           down    left

3           4           left    down
3           2           right   up

4           3           up      right

4           1           left    right
5           2           right   left

5           6           down    left

6           1           left    down
6           5           right   up

6           2           down    down
"""
#           0       1       2       3
# dirs = ["right", "down", "left", "up"]
MATCH = {
    (1, 6): 0,
    (2, 6): 3,
    (1, 4): 0,
    (2, 5): 2,
    (2, 3): 2,
    (3, 4): 1,
    (3, 2): 3,
    (4, 3): 0,
    (4, 1): 0,
    (5, 2): 2,
    (5, 6): 2,
    (6, 1): 1,
    (6, 5): 3,
    (6, 2): 1,
}

TEST_MATCH = {
    (1, 2): 1,

    (1, 3): 1,
    (1, 6): 2,

    (2, 1): 1,
    (3, 1): 0,
    (2, 6): 3,
    (4, 6): 1,

    (2, 5): 3,
    (3, 5): 0,

    (6, 4): 2,

    (5, 3): 3,
    (6, 1): 2,

    (5, 2): 3,
    (6, 2): 0,
}



DIFFS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS = ["up", "down", "left", "right"]


@dataclass
class Node:
    x: int
    y: int
    grid_num: int

    left: "Node" = None
    right: "Node" = None
    up: "Node" = None
    down: "Node" = None

    leftmost: "Node" = None
    rightmost: "Node" = None
    upmost: "Node" = None
    downmost: "Node" = None

    def __str__(self):
        return f"Node(x={self.x}, y={self.y}, grid_num={self.grid_num})"

    def __hash__(self):
        return id(self)


def get_first(it):
    for x, val in enumerate(it):
        if val != ' ':
            return x


def set_most(node: Node, next_attr, set_attr):
    cur = node
    if getattr(cur, set_attr) is not None:
        return
    prev = None
    nodes = set()
    while cur and getattr(cur, set_attr) is None and cur not in nodes:
        nodes.add(cur)
        prev = cur
        cur = getattr(cur, next_attr)

    for node in nodes:
        if getattr(prev, next_attr) is None:
            setattr(node, set_attr, prev)
        else:
            setattr(node, set_attr, node)


def build_graph(lines) -> Node:
    N = len(lines)
    M = max(map(len, lines))
    lines = list(map(list, lines))
    for line in lines:
        if len(line) < M:
            line.extend(' ' for _ in range(M - len(line)))
    print(N, M)

    grid = [[None] * M for _ in range(N)]

    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            if val != '.':
                continue
            grid[y][x] = Node(x=x, y=y, grid_num=0)

    # link neighbors
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node is None:
                continue
            for (dy, dx), attr in zip(DIFFS, DIRS):
                ny = y + dy
                nx = x + dx
                if 0 <= ny < N and 0 <= nx < M and grid[ny][nx] is not None:
                    setattr(node, attr, grid[ny][nx])

    # link corners
    for y, line in enumerate(lines):
        x_left = get_first(line)
        x_right = M - get_first(reversed(line)) - 1
        left = grid[y][x_left]
        right = grid[y][x_right]
        if left is None or right is None:
            continue
        left.left = right
        right.right = left

    for x in range(M):
        y_top = get_first(lines[y][x] for y in range(N))
        y_bottom = N - get_first(lines[y][x] for y in range(N-1, -1, -1)) - 1
        top = grid[y_top][x]
        bottom = grid[y_bottom][x]
        if top is None or bottom is None:
            continue
        top.up = bottom
        bottom.down = top

    print(1)
    for y, _ in enumerate(lines):
        for x in range(M):
            if grid[y][x] is None:
                continue
            set_most(grid[y][x], "right", "rightmost")

        for x in range(M-1, -1, -1):
            if grid[y][x] is None:
                continue
            set_most(grid[y][x], "left", "leftmost")

    print(2)
    for x in range(M):
        for y in range(N):
            if grid[y][x] is None:
                continue
            set_most(grid[y][x], "down", "downmost")

        for y in range(N-1, -1, -1):
            if grid[y][x] is None:
                continue
            set_most(grid[y][x], "up", "upmost")

    print(3)
    x_start = get_first(lines[0])
    return grid[0][x_start]


def parse_input(s: str):
    lines = s.splitlines()
    path = [
        int(match) if match.isnumeric() else match
        for match in re.findall(r"(\d+|[RL])", lines[-1])
    ]
    start = build_graph(lines[:-2])
    return start, path


def part_one(start, path):
    print(start, path)
    dirs = ["right", "down", "left", "up"]
    direction = 0
    cur = start

    for val in path:
        if isinstance(val, str):
            if val == "L":
                diff = -1
            else:
                diff = 1
            direction = (4 + direction + diff) % 4
            continue

        for _ in range(val):
            attr = dirs[direction]
            nxt = getattr(cur, attr)
            if nxt is None:
                break
            key = (cur.grid_num, nxt.grid_num)
            if key in MATCH:
                print((cur.grid_num, nxt.grid_num), direction,  MATCH[key])
                direction = MATCH[key]
            cur = nxt
        print(cur, dirs[direction], val, getattr(cur, dirs[direction]))

    rv = 1000 * (cur.y + 1) + 4 * (cur.x + 1) + direction
    print(rv, cur)
    return rv


def parse_test_cube(s: str):
    lines = s.splitlines()
    path = [
        int(match) if match.isnumeric() else match
        for match in re.findall(r"(\d+|[RL])", lines[-1])
    ]
    lines = lines[:-2]

    g1 = parse_grid(lines, 8, 0, 4, 1)
    g2 = parse_grid(lines, 0, 4, 4, 2)
    g3 = parse_grid(lines, 4, 4, 4, 3)
    g4 = parse_grid(lines, 8, 4, 4, 4)
    g5 = parse_grid(lines, 8, 8, 4, 5)
    g6 = parse_grid(lines, 12, 8, 4, 6)

    connect_grids(g4, g1, "up", "down")
    connect_grids(g3, rotate_left(g1), "up", "left")
    connect_grids(g2, rotate_twice(g1), "up", "up")
    connect_grids(rotate_left(g6), rotate_right(g1), "right", "right")

    connect_grids(rotate_left(g2), rotate_left(g3), "right", "left")
    connect_grids(rotate_left(g3), rotate_left(g4), "right", "left")
    connect_grids(rotate_left(g4), rotate_twice(g6), "right", "up")
    connect_grids(rotate_right(g2), g6, "left", "down")

    connect_grids(g5, g4, "up", "down")
    connect_grids(rotate_right(g5), g3, "left", "down")
    connect_grids(rotate_twice(g5), g2, "down", "down")
    connect_grids(rotate_left(g5), rotate_left(g6), "right", "left")

    print(g1[0][0], g1[-1][1].down)
    print(g2[0][0])
    print(g3[0][0])
    print(g4[0][0], g4[0][1].up)
    print(g5[0][0])
    print(g6[0][0])
    return g1[0][0], path


def parse_cube(s: str):
    lines = s.splitlines()
    path = [
        int(match) if match.isnumeric() else match
        for match in re.findall(r"(\d+|[RL])", lines[-1])
    ]
    lines = lines[:-2]
    g1 = parse_grid(lines, 50, 0, 50, 1)
    g2 = parse_grid(lines, 100, 0, 50, 2)
    g3 = parse_grid(lines, 50, 50, 50, 3)
    g4 = parse_grid(lines, 0, 100, 50, 4)
    g5 = parse_grid(lines, 50, 100, 50, 5)
    g6 = parse_grid(lines, 0, 150, 50, 6)

    connect_grids(g3, g1, "up", "down")
    connect_grids(rotate_right(g4), rotate_left(g1), "left", "left")
    connect_grids(rotate_right(g6), rotate_twice(g1), "left", "up")
    connect_grids(rotate_right(g2), rotate_right(g1), "left", "right")

    connect_grids(rotate_right(g3), rotate_twice(g4), "left", "up")
    connect_grids(g6, g4, "up", "down")
    connect_grids(rotate_twice(g6), rotate_twice(g2), "down", "up")
    connect_grids(rotate_left(g3), g2, "right", "down")

    connect_grids(g5, g3, "up", "down")
    connect_grids(rotate_right(g5), rotate_right(g4), "left", "right")
    connect_grids(rotate_left(g5), rotate_right(g2), "right", "right")
    connect_grids(rotate_twice(g5), rotate_right(g6), "down", "right")

    return g1[0][0], path


def parse_grid(lines, x, y, size, grid_num):
    grid = [[None] * size for _ in range(size)]

    for dy in range(size):
        for dx in range(size):
            nx = x + dx
            ny = y + dy
            if lines[ny][nx] != '.':
                continue
            # print(x, y, dx, dy, nx, ny)
            grid[dy][dx] = Node(x=nx, y=ny, grid_num=grid_num)

    # link neighbors
    for gy, row in enumerate(grid):
        for gx, node in enumerate(row):
            if node is None:
                continue
            for (dy, dx), attr in zip(DIFFS, DIRS):
                ny = gy + dy
                nx = gx + dx
                if 0 <= ny < size and 0 <= nx < size and grid[ny][nx] is not None:
                    setattr(node, attr, grid[ny][nx])
    return grid


def connect_grids(bottom, top, first, second):
    for n1, n2 in zip(bottom[0], top[-1]):
        if n1 is None or n2 is None:
            continue

        setattr(n1, first, n2)
        setattr(n2, second, n1)


def rotate_right(grid):
    """
    1,2,3
    4,5,6
    7,8,9
    """
    grid = [row.copy() for row in grid]
    N = len(grid)
    for i in range(N):
        for j in range(i, N):
            grid[i][j], grid[j][i] = grid[j][i], grid[i][j]

    for i in range(N):
        for j in range(N // 2):
            grid[i][j], grid[i][N - j - 1] = grid[i][N - j - 1], grid[i][j]

    return grid


def rotate_left(grid):
    grid = rotate_right(grid)
    grid = rotate_right(grid)
    grid = rotate_right(grid)
    return grid


def rotate_twice(grid):
    grid = rotate_right(grid)
    grid = rotate_right(grid)
    return grid


if __name__ == '__main__':
    # assert part_one(*parse_input(TEST)) == 6032
    # print(part_one(*parse_input(open("input").read())))

    # assert part_one(*parse_test_cube(TEST)) == 5031
    print(part_one(*parse_cube(open("input").read())))

    print("DONE")
