import ast
from functools import cmp_to_key

TEST = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def parse_input(s: str):
    for pair in s.split("\n\n"):
        a, b = pair.splitlines()
        yield ast.literal_eval(a), ast.literal_eval(b)


def part_one(pairs):
    result = 0
    for i, (a, b) in enumerate(pairs, start=1):
        tmp = compare(a, b)
        if tmp == -1:
            result += i
        # print(i, tmp)

    return result


def compare(first, second):
    for a, b in zip(first, second):
        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                return -1
            if a > b:
                return 1
            continue
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]

        if (rv := compare(a, b)) != 0:
            return rv

    if len(first) < len(second):
        return -1
    if len(first) > len(second):
        return 1
    return 0


def part_two(s: str):
    packets = [ast.literal_eval(line) for line in s.splitlines() if line]
    packets.append([[2]])
    packets.append([[6]])
    packets.sort(key=cmp_to_key(compare))

    first = packets.index([[2]])
    second = packets.index([[6]])
    print(first, second)
    return (first+1) * (second+1)


if __name__ == '__main__':
    assert part_one(parse_input(TEST)) == 13
    print("part_one", part_one(parse_input(open("input").read())))

    assert part_two(TEST) == 140
    print(part_two(open("input").read()))

    print("DONE")
