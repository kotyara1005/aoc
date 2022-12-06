from collections import Counter


def decr(counter, key):
    counter[key] -= 1
    if counter[key] == 0:
        del counter[key]


def find_marker(line, size):
    counter = Counter(line[:size])

    for i, (remove, add) in enumerate(zip(line, line[size:]), start=size):
        if len(counter) == size:
            return i

        decr(counter, remove)
        counter[add] += 1
    return -1


if __name__ == '__main__':
    assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

    print(find_marker(open("input").read(), 4))

    assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

    print(find_marker(open("input").read(), 14))
