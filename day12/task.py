from typing import Tuple
from collections import defaultdict

TEST = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def get_edges(mat, x, y):
    N = len(mat)
    M = len(mat[0])
    height = ord(mat[x][y])

    for dx, dy in DIRS:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < N and 0 <= ny < M:
            nh = ord(mat[nx][ny])
            if nh - height <= 1:
                yield (x, y), (nx, ny)


def parse_input(s: str) -> Tuple[list, dict, tuple, tuple]:
    mat = list(map(list, s.splitlines()))
    N = len(mat)
    M = len(mat[0])
    start = None
    stop = None

    for x in range(N):
        for y in range(M):
            if mat[x][y] == "S":
                mat[x][y] = 'a'
                start = x, y
            if mat[x][y] == "E":
                mat[x][y] = 'z'
                stop = x, y

    edges = []
    for x in range(N):
        for y in range(M):
            edges.extend(get_edges(mat, x, y))

    graph = defaultdict(list)

    for a, b in edges:
        graph[a].append(b)

    return mat, graph, start, stop


def part_one(_, graph, start, stop):
    """BFS"""
    q = [start]
    visied = set()
    result = 0
    while q:
        nq = []
        for node in q:
            if node in visied:
                continue
            visied.add(node)
            if node == stop:
                return result
            nq.extend(graph[node])
        q = nq
        result += 1
    return None


def part_two(mat, graph, _, stop):
    """BFS"""
    q = [(x, y) for x in range(len(mat)) for y in range(len(mat[0])) if mat[x][y] == 'a']
    visied = set()
    result = 0
    while q:
        nq = []
        for node in q:
            if node in visied:
                continue
            visied.add(node)
            if node == stop:
                return result
            nq.extend(graph[node])
        q = nq
        result += 1
    print(result)
    return None


if __name__ == '__main__':
    assert part_one(*parse_input(TEST)) == 31
    print(part_one(*parse_input(open("input").read())))

    assert part_two(*parse_input(TEST)) == 29
    print(part_two(*parse_input(open("input").read())))

    print("DONE")
