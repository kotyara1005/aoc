import re

TEST = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


REGEX = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


def parse_input(s: str):
    result = []
    for line in s.splitlines():
        result.append(tuple(map(int, REGEX.match(line).groups())))

    return result


def get_manhattan_distance(sx, sy, bx, by):
    return abs(sx - bx) + abs(sy - by)


def get_interval(sx, sy, bx, by, y):
    radius = get_manhattan_distance(sx, sy, bx, by)
    rng = radius - abs(sy - y)
    if rng <= 0:
        return None

    # print(sx, sy, bx, by, radius, rng, (sx - rng, sx + rng))
    return sx - rng, sx + rng


def merge_intervals(intervals):
    intervals.sort()
    result = [intervals[0]]

    for a, b in intervals[1:]:
        if result[-1][0] <= a <= b <= result[-1][1]:
            continue
        if result[-1][1] == a - 1:
            result[-1] = (result[-1][0], b)
        elif result[-1][0] <= a <= result[-1][1] <= b:
            result[-1] = (result[-1][0], max(result[-1][1], b))
        else:
            result.append((a, b))

    return result


def part_one(pairs, line_num):
    # print(pairs)
    min_x = min(min(p[0], p[2]) for p in pairs)
    max_x = max(max(p[0], p[2]) for p in pairs)
    min_y = min(min(p[1], p[3]) for p in pairs)
    max_y = max(max(p[1], p[3]) for p in pairs)

    intervals = [
        interval
        for sx, sy, bx, by in pairs
        if (interval := get_interval(sx, sy, bx, by, line_num)) is not None
    ]
    # print(sorted(intervals))

    intervals = merge_intervals(intervals)
    print(intervals)

    return sum(b - a for a, b in intervals)


def part_two(pairs, max_y):
    for y in range(max_y+1):
        intervals = [
            interval
            for sx, sy, bx, by in pairs
            if (interval := get_interval(sx, sy, bx, by, y)) is not None
        ]
        intervals = merge_intervals(intervals)
        if len(intervals) == 2:
            x = intervals[0][1]+1
            print(x, y, x * 4_000_000 + y)
            return x * 4_000_000 + y


if __name__ == '__main__':
    assert part_one(parse_input(TEST), 10) == 26
    print(part_one(parse_input(open("input").read()), 2000000))

    assert part_two(parse_input(TEST), 20) == 56000011
    print(part_two(parse_input(open("input").read()), 4000000))
    print("DONE")
