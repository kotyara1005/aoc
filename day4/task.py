TEST = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def parse(line):
    first, second = line.split(",")
    first = first.split("-")
    second = second.split("-")
    return int(first[0]), int(first[1]), int(second[0]), int(second[1])


def main(lines):
    result = 0

    for line in lines:
        s1, e1, s2, e2 = parse(line)
        if s1 > s2:
            s1, e1, s2, e2 = s2, e2, s1, e1

        if s2 <= e1:
            result += 1

    print("part 1", result)


if __name__ == '__main__':
    main(TEST.splitlines())
    main(open("input").read().splitlines())
