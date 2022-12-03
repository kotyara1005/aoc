import string

PRIORITY = {l: i for i, l in enumerate(string.ascii_letters, start=1)}
print(PRIORITY)

TEST = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def main(lines: list[str]):
    result_1 = 0
    for line in lines:
        mid = len(line) // 2
        first = set(line[:mid])
        second = set(line[mid:])
        common = first.intersection(second).pop()
        # print(common, PRIORITY[common])
        result_1 += PRIORITY[common]

    print("part 1", result_1)

    result_2 = 0

    for first, second, third in zip(lines[::3], lines[1::3], lines[2::3]):
        common = set(first).intersection(second).intersection(third).pop()
        result_2 += PRIORITY[common]

    print("part 2", result_2)


if __name__ == "__main__":
    main(TEST.splitlines())
    main(open("input").read().splitlines())
