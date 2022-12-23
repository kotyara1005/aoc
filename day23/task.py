from collections import deque, defaultdict

TEST = """\
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""

TEST_RESULT = """\
......#.....
..........#.
.#.#..#.....
.....#......
..#.....#..#
#......##...
....##......
.#........#.
...#.#..#...
............
...#..#..#.."""

TEST1 = """\
.....
..##.
..#..
.....
..##.
....."""


def parse_input(s: str) ->list[tuple[int, int]]:
    elfs = []

    for x, line in enumerate(s.splitlines()):
        for y, val in enumerate(line):
            if val == "#":
                elfs.append((x, y))
    return elfs


DIRS = [
    [(-1, -1), (-1, 0), (-1, 1)],
    [(1, -1), (1, 0), (1, 1)],
    [(-1, -1), (0, -1), (1, -1)],
    [(-1, 1), (0, 1), (1, 1)],
]


DIFFS = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx != 0 or dy != 0]


def has_neighbors(elfs, x, y):
    for dx, dy in DIFFS:
        if (x+dx, y+dy) in elfs:
            return True
    return False


def check_progress(elfs):
    x_min = min(x for x, y in elfs)
    x_max = max(x for x, y in elfs)
    y_min = min(y for x, y in elfs)
    y_max = max(y for x, y in elfs)

    square = (x_max - x_min + 1) * (y_max - y_min + 1)
    # print(x_min, x_max, y_min, y_max)
    return square - len(elfs)
    # return square


def debug(elfs):
    for x in range(15):
        for y in range(15):
            val = '.'
            if (x, y) in elfs:
                val = '#'
            print(val, end='')
        print()
    print()


def part_one(elfs):
    elfs = set(elfs)
    dirs = deque(DIRS)
    # debug(elfs)
    for i in range(1_000_000_000):
        proposals = defaultdict(list)
        for elf in elfs:
            if not has_neighbors(elfs, *elf):
                proposals[elf].append(elf)
                continue

            for diffs in dirs:
                if all((elf[0]+dx, elf[1]+dy) not in elfs for dx, dy in diffs):
                    pos = (elf[0]+diffs[1][0], elf[1]+diffs[1][1])
                    proposals[pos].append(elf)
                    break
            else:
                proposals[elf].append(elf)

        nxt_elfs = set()
        moved = False
        for pos, candidates in proposals.items():
            if len(candidates) == 1:
                nxt_elfs.add(pos)
                if pos != candidates[0]:
                    moved = True
            else:
                nxt_elfs.update(candidates)

        elfs = nxt_elfs
        dirs.rotate(-1)
        if i == 9:
            print("part_one", check_progress(elfs))

        if i % 100:
            print(i, moved)
        if not moved:
            print("part_two", i+1)
            break


if __name__ == '__main__':
    assert check_progress(parse_input(TEST_RESULT)) == 110
    part_one(parse_input(TEST))
    # print(part_one(parse_input(TEST1)))
    print(part_one(parse_input(open("input").read())))

    print("DONE")
