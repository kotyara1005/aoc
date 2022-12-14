TEST = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def parse_input(s: str):
    result = []
    for line in s.splitlines():
        result.append([tuple(map(int, l.split(','))) for l in line.split(" -> ")])

    visited = set()

    for line in result:
        for (x1, y1), (x2, y2) in zip(line, line[1:]):
            if x1 == x2:
                diff = 1 if y2 > y1 else -1
                visited.update((x1, y) for y in range(y1, y2+diff, diff))
            elif y1 == y2:
                diff = 1 if x2 > x1 else -1
                visited.update((x, y1) for x in range(x1, x2+diff, diff))
            else:
                raise Exception()

    return visited


def part_one(visited):
    max_depth = max(r[1] for r in visited) + 1
    result = 0
    # print(max_depth, visited)

    while True:
        prev = None
        cur = (500, 0)
        while prev != cur and cur[1] <= max_depth:
            prev = cur
            for dx in (0, -1, 1):
                nxt = (cur[0] + dx, cur[1] + 1)
                if nxt not in visited:
                    cur = nxt
                    break
        # print(cur)
        if cur[1] > max_depth:
            break
        result += 1
        visited.add(cur)

    # print(result)
    return result


def part_two(visited):
    floor = max(r[1] for r in visited) + 2
    result = 0
    cur = None

    while cur != (500, 0):
        prev = None
        cur = (500, 0)
        while prev != cur and cur[1] != floor - 1:
            prev = cur
            for dx in (0, -1, 1):
                nxt = (cur[0] + dx, cur[1] + 1)
                if nxt not in visited:
                    cur = nxt
                    break
        result += 1
        visited.add(cur)
        # print(prev, cur)

    print(result)
    return result


if __name__ == '__main__':
    # assert part_one(parse_input(TEST)) == 24
    # print(part_one(parse_input(open("input").read())))

    assert part_two(parse_input(TEST)) == 93
    print(part_two(parse_input(open("input").read())))

    print("DONE")
