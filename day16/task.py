import re
from pprint import pprint
from typing import NamedTuple
import time
from contextlib import ContextDecorator


class TimeIt(ContextDecorator):
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(time.time() - self.start)
        return True


TEST = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

REGEX = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([, \w]+)")


def parse_input(s: str):
    edges = [REGEX.match(line).groups() for line in s.splitlines()]
    edges = [(name, int(rate), set(paths.split(', '))) for name, rate, paths in edges]

    rates = {name: rate for name, rate, paths in edges}
    names = sorted(name for name, _, _ in edges)
    paths = {name: dict.fromkeys(names, float("inf")) for name in names}

    for name, _, paths_ in edges:
        paths[name][name] = 0
        for nxt in paths_:
            paths[nxt][name] = paths[name][nxt] = 1

    for n1 in names:
        for n2 in names:
            for n3 in names:
                paths[n3][n2] = paths[n2][n3] = min(paths[n3][n2], paths[n2][n3], paths[n2][n1] + paths[n1][n3])

    # print('\t','\t'.join(names))
    # for n1 in names:
    #     print(n1, '\t', end='')
    #     for n2 in names:
    #         print(paths[n1][n2], '\t', end='')
    #     print()
    #
    # pprint(rates)
    return paths, rates


@TimeIt()
def part_one(paths, rates):
    opened = set(name for name, rate in rates.items() if rate == 0)

    def backtrack(name, time, prev):
        if time == 0:
            return prev
        if time < 0:
            return 0

        prev += rates[name] * (time - 1)
        result = prev
        opened.add(name)

        for nxt in paths:
            if nxt in opened:
                continue

            result = max(result, backtrack(nxt, time - 1 - paths[name][nxt], prev))

        opened.discard(name)
        return result

    rv = backtrack('AA', 31, 0)
    return rv


class Task(NamedTuple):
    time: int
    dest: str


@TimeIt()
def part_two(paths, rates):
    opened = set(name for name, rate in rates.items() if rate == 0)

    def backtrace(task1, task2, prev):
        # print(task1, task2, prev)
        task1, task2 = sorted([task1, task2], reverse=True)
        result = prev
        time, name = task1
        for nxt in paths:
            if nxt in opened:
                continue

            nxt_time = time - 1 - paths[name][nxt]
            if nxt_time < 0:
                continue

            opened.add(nxt)
            result = max(
                result,
                backtrace(
                    Task(nxt_time, nxt),
                    task2,
                    prev + nxt_time * rates[nxt],
                ),
            )
            opened.discard(nxt)

        return result

    return backtrace(
        Task(26, 'AA'),
        Task(26, 'AA'),
        0,
    )


if __name__ == '__main__':
    assert part_one(*parse_input(TEST)) == 1651
    print(part_one(*parse_input(open("input").read())))

    assert part_two(*parse_input(TEST)) == 1707
    print(part_two(*parse_input(open("input").read())))
    print("DONE")
