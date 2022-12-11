TEST = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

TEST0 = """\
noop
addx 3
addx -5"""


def part_one(lines):
    result = 0
    value = 1
    cycle = 0
    threshold = 20

    def check():
        # print(cycle, value)
        nonlocal threshold, result
        if threshold == cycle:
            print(threshold, value, value * threshold)
            result += value * threshold
            threshold += 40

    check()
    for line in lines:
        ops = line.split(" ")
        if ops[0] == "noop":
            cycle += 1
            check()
        elif ops[0] == "addx":
            cycle += 1
            check()
            cycle += 1
            check()
            value += int(ops[1])

    print(result, cycle, len(lines))
    return result


def part_two(lines):
    result = []
    value = 1
    cycle = 0

    def draw():
        line_num = (cycle-1) // 40
        pos = (cycle-1) % 40
        print((cycle), pos, line_num, value)

        if len(result) == line_num:
            result.append([])

        char = '.'
        if pos in {value-1, value, value+1}:
            char = '#'
        result[-1].append(char)

    # draw()
    for line in lines:
        ops = line.split(" ")
        if ops[0] == "noop":
            cycle += 1
            draw()
        elif ops[0] == "addx":
            cycle += 1
            draw()
            cycle += 1
            draw()
            value += int(ops[1])
        # if cycle >= 40:
        #     break

    print('\n'.join(''.join(line) for line in result))
    print(len(result[0]))
    return '\n'.join(''.join(line) for line in result)


if __name__ == '__main__':
    assert part_one(TEST.splitlines()) == 13140
    part_one(TEST0.splitlines())
    print(part_one(open("input").read().splitlines()))

    assert part_two(TEST.splitlines()) == """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

    print(part_two(open("input").read().splitlines()))
    print("DONE")
