TEST = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


TEST_P2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def parse_input(lines):
    for line in lines:
        dr, count = line.split(" ")
        dx = dy = 0
        if dr == "U":
            dy = 1
        elif dr == "D":
            dy = -1
        elif dr == "R":
            dx = 1
        elif dr == "L":
            dx = -1
        yield dx, dy, int(count)


def get_diff(a, b):
    if a - b < 0:
        return -1
    return 1


def get_tail_move(tail, head):
    hx, hy = head
    tx, ty = tail
    dx = dy = 0

    diff_x = abs(hx - tx)
    diff_y = abs(hy - ty)

    if diff_y == 0 and diff_x > 1:
        dx = get_diff(hx, tx)
    elif diff_x == 0 and diff_y > 1:
        dy = get_diff(hy, ty)
    elif diff_y and diff_x and (diff_y > 1 or diff_x > 1):
        dx = get_diff(hx, tx)
        dy = get_diff(hy, ty)

    return dx, dy


def debug(tail, head, N=10, M=9):
    mat = [['.']*N for _ in range(M)]

    mat[tail[0]][tail[1]] = 'T'
    mat[head[0]][head[1]] = 'H'

    for row in reversed(mat):
        print(''.join(row))
    print()


def part_one(commands):
    visited = set()
    head = [0, 0]
    tail = [0, 0]

    for dx, dy, count in commands:
        for _ in range(count):
            head[0] += dx
            head[1] += dy

            tdx, tdy = get_tail_move(tail, head)
            tail[0] += tdx
            tail[1] += tdy
            # print(tail, head)
            visited.add(tuple(tail))
            # debug(tail, head)

    # print(len(visited))
    return len(visited)


def debug_p2(rope, N=40, M=30):
    mat = [['.']*N for _ in range(M)]

    for i, node in enumerate(rope):
        placeholder = str(i)
        if i == 0:
            placeholder = 'H'
        if i == len(rope) - 1:
            placeholder = 'T'

        if mat[node[1]+10][node[0]+10] == '.':
            mat[node[1]+10][node[0]+10] = placeholder

    for row in reversed(mat):
        print(''.join(row))
    print()


def part_two(commands):
    visited = set()
    rope = [[0, 0] for _ in range(10)]

    for dx, dy, count in commands:
        for _ in range(count):
            rope[0][0] += dx
            rope[0][1] += dy

            for head, tail in zip(rope, rope[1:]):
                tdx, tdy = get_tail_move(tail, head)
                tail[0] += tdx
                tail[1] += tdy
                # print(tail, head)

            visited.add(tuple(rope[-1]))
        # print(len(visited))
        # print(sorted(visited))
        # print(rope)
        # debug_p2(rope)

    print(len(visited))
    # print(sorted(visited))
    return len(visited)


if __name__ == '__main__':
    assert part_one(parse_input(TEST.splitlines())) == 13
    print(part_one(parse_input(open("input").read().splitlines())))

    assert part_two(parse_input(TEST_P2.splitlines())) == 36
    print(part_two(parse_input(open("input").read().splitlines())))
