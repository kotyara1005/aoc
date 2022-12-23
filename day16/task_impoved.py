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
        return False


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


def set_bit(s: int, num: int) -> int:
    return s | (1 << num)


def get_bit(s: int, num: int) -> int:
    return bool(s & (1 << num))


def find_all_paths(edges):
    # Floyd–Warshall algorithm
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
    return paths, names


def parse_input(s: str):
    edges = [REGEX.match(line).groups() for line in s.splitlines()]
    edges = [(name, int(rate), set(paths.split(', '))) for name, rate, paths in edges]

    rates = {name: rate for name, rate, paths in edges}
    paths, names = find_all_paths(edges)

    closed = sorted(name for name, rate in rates.items() if rate > 0 or name == "AA")

    valve_map = {name: i for i, name in enumerate(closed)}
    N = len(valve_map)

    np = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            np[i][j] = paths[closed[i]][closed[j]]

    paths = np
    # print(*paths, sep='\n')
    rates = [rates[closed[i]] for i in range(N)]

    # print('\t','\t'.join(names))
    # for n1 in names:
    #     print(n1, '\t', end='')
    #     for n2 in names:
    #         print(paths[n1][n2], '\t', end='')
    #     print()

    # pprint(rates)
    return paths, rates


# @TimeIt()
def find_best_path(paths, rates, cache, opened=0, start_time=31):
    def backtrack(node, time, opened, prev):
        key = (node, time, opened, prev)
        if key in cache:
            return cache[key]

        if time == 0:
            return prev

        if time < 0:
            return 0

        prev += rates[node] * (time - 1)
        result = prev
        opened = set_bit(opened, node)
        for nxt in range(len(paths)):
            if get_bit(opened, nxt):
                continue

            loc = backtrack(nxt, time - 1 - paths[node][nxt], opened, prev)
            result = max(result, loc)

        cache[key] = result
        return result

    rv = backtrack(0, start_time, opened, 0)
    # print(rv)
    return rv


@TimeIt()
def part_two(paths, rates):
    N = len(paths)
    print(N, 2**N)
    results = [0]*(2**N)
    # cache = {}
    for i in range(2**N):
        if i % 2 == 1:
            continue
        if i % 100 == 0:
            print(i, bin(i), bin(~i&(2**N-1)))
        results[i] = find_best_path(paths, rates, {}, i, start_time=27)
    rv = -1
    for k in range(len(results)):
        if k % 2 == 1:
            k -= 1
        m = ~k & (2 ** N - 1)
        m -= 1
        print(N, k, m)
        loc = results[k] + results[m]
        # print(bin(k), bin(m), results[k], results[m], loc, m & k)
        rv = max(rv, loc)

    # rv = max(results[k] + results[~k&(2**N-1)] for k in results)
    print(rv, results[0], results[2**N-1])
    return rv


if __name__ == '__main__':
    """
    0.0028939247131347656
    1.9716150760650635
    2359
    
    part two 
    0.0058820247650146484  
    
    2999
    DONE
    
    
    0.0061800479888916016
    2359
    3.344844102859497
    DONE
    """
    assert find_best_path(*parse_input(TEST)) == 1651
    assert find_best_path(*parse_input(open("input").read())) == 2359

    assert part_two(*parse_input(TEST)) == 1707
    print(part_two(*parse_input(open("input").read())))
    print("DONE")
