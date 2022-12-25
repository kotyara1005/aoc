TEST = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]

DIR_MAP = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def parse_input(s: str):
    lines = s.splitlines()
    N = len(lines)
    M = len(lines[0])

    blizzards = []

    for x, line in enumerate(lines):
        for y, val in enumerate(line):
            if val == "." or val == "#":
                continue
            blizzards.append((x, y, *DIR_MAP[val]))

    start = (0, 1)
    stop = (N - 1, M - 2)
    return blizzards, start, stop, N, M


def get_obstacles(blizzards):
    return frozenset((i, j) for i, j, *_ in blizzards)


def get_next_state(blizzards, N, M):
    result = []
    i_map = {0: N - 2, N - 1: 1}
    j_map = {0: M - 2, M - 1: 1}

    for i, j, di, dj in blizzards:
        ni = i + di
        nj = j + dj

        ni = i_map.get(ni, ni)
        nj = j_map.get(nj, nj)
        result.append((ni, nj, di, dj))

    return result


def iter_states(blizzards, N, M):
    while True:
        blizzards = get_next_state(blizzards, N, M)
        yield get_obstacles(blizzards)


def get_next_positions(i, j, N, M):
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
        ni = i + di
        nj = j + dj
        if (0 < ni < N - 1 and 0 < nj < M - 1) or (ni == N - 1 and nj == M - 2) or (ni == 0 and nj == 1):
            yield ni, nj


def part_one(blizzards, start, stop, N, M):
    q = [start]

    for num, obstacles in enumerate(iter_states(blizzards, N, M)):
        # print(num, q, obstacles, N, M)
        nxt_q = set()
        for pos in q:
            # print(pos)
            if pos == stop:
                return num

            for nxt in get_next_positions(*pos, N, M):
                # print(pos,/ nxt)
                if nxt in obstacles:
                    continue

                nxt_q.add(nxt)
        q = nxt_q
        if num > 1_000_000:
            break
        if not q:
            print("no pos", num)
            break


def part_two(blizzards, start, stop, N, M):
    q = [start]
    stops = [stop, start, stop]

    for num, obstacles in enumerate(iter_states(blizzards, N, M)):
        # print(num, q, obstacles, N, M)
        nxt_q = set()
        for pos in q:
            # print(pos)
            if pos == stops[-1]:
                # print(pos, stops[-1], num, stops)
                stops.pop()
                nxt_q = {pos}
                if stops:
                    break
                else:
                    return num

            for nxt in get_next_positions(*pos, N, M):
                # print(pos,/ nxt)
                if nxt in obstacles:
                    continue

                nxt_q.add(nxt)
        q = nxt_q
        if num > 1_000_000:
            break
        if not q:
            print("no pos", num)
            break


if __name__ == '__main__':
    assert part_one(*parse_input(TEST)) == 18
    print(part_one(*parse_input(open("input").read())))

    assert part_two(*parse_input(TEST)) == 54
    print(part_two(*parse_input(open("input").read())))
    print("DONE")
