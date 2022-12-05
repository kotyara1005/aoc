import re

TEST = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

REGEX = re.compile(r"move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)")


def parse_stacks(lines):
    data = [list(l)[1::4] for l in lines[:-1]]
    # print(*data, sep='\n')
    M = len(data)
    N = max(map(len, data))
    for l in data:
        l += [' '] * (N-len(l))

    print(*data, sep='\n')
    stacks = []
    for i in range(N):
        stacks.append([data[j][i] for j in range(M) if data[j][i] != ' '])
        stacks[-1].reverse()

    print()
    print(*stacks, sep='\n')
    print()
    return stacks


def parse_bottom(lines):
    for line in lines:
        match = REGEX.match(line).groups()
        yield int(match[0]), int(match[1])-1, int(match[2])-1


def main(lines):
    idx = lines.index('')
    # print(idx)
    head = lines[:idx]
    print(*head, sep='\n')
    bottom = lines[idx+1:]

    stacks = parse_stacks(head)

    for count, from_, to_ in parse_bottom(bottom):
        # print(count, from_, to_)
        # print(*stacks, sep='\n')
        # print()
        # for _ in range(count):
        #     # print(stacks[from_])
        #     stacks[to_].append(stacks[from_].pop())
        stacks[to_] += stacks[from_][-count:]
        stacks[from_] = stacks[from_][:-count]

        # print(*stacks, sep='\n')
        # print()

    print(''.join(st[-1] for st in stacks))


if __name__ == '__main__':
    main(TEST.splitlines())
    main(open("input").read().splitlines())
