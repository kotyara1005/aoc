from itertools import chain

TEST = """\
30373
25512
65332
33549
35390"""


def parse_input(s: str):
    return [list(map(int, line)) for line in s.splitlines()]


def part_one(mat):
    N = len(mat)
    M = len(mat[0])

    visible = [[False] * M for _ in range(N)]

    for i, row in enumerate(mat):
        obstacle = -1
        for j, val in enumerate(row):
            if obstacle < val:
                obstacle = val
                visible[i][j] = True

        obstacle = -1
        for j, val in zip(range(M-1, -1, -1), reversed(row)):
            if obstacle < val:
                obstacle = val
                visible[i][j] = True

    for j in range(M):
        obstacle = -1
        for i in range(N):
            if obstacle < mat[i][j]:
                obstacle = mat[i][j]
                visible[i][j] = True

        obstacle = -1
        for i in range(N-1, -1, -1):
            if obstacle < mat[i][j]:
                obstacle = mat[i][j]
                visible[i][j] = True

    result = sum(chain.from_iterable(visible))

    return result


def compute_scenic(mat, i, j):
    N = len(mat)
    M = len(mat[0])
    val = mat[i][j]
    a = b = c = d = 0

    for p in range(i+1, N):
        a += 1
        if mat[p][j] >= val:
            break

    for p in range(i-1, -1, -1):
        b += 1
        if mat[p][j] >= val:
            break

    for p in range(j + 1, M):
        c += 1
        if mat[i][p] >= val:
            break

    for p in range(j - 1, -1, -1):
        d += 1
        if mat[i][p] >= val:
            break

    return a * b * c * d


def part_two(mat):
    N = len(mat)
    M = len(mat[0])
    result = 0

    for i in range(N):
        for j in range(M):
            result = max(result, compute_scenic(mat, i, j))

    return result


if __name__ == '__main__':
    assert part_one(parse_input(TEST)) == 21
    print(part_one(parse_input(open("input").read())))

    assert compute_scenic(parse_input(TEST), 1,2) == 4
    assert compute_scenic(parse_input(TEST), 3,2) == 8
    assert part_two(parse_input(TEST)) == 8
    print(part_two(parse_input(open("input").read())))
