from itertools import cycle
from typing import Set, Tuple, NamedTuple, DefaultDict
from collections import Counter, defaultdict
import time

TEST = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

# TODO maybe it's inverted
SHAPES = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),  # -
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2),),  # +
    ((2, 2),
     (2, 1),
     (0, 0), (1, 0), (2, 0)),
    # l-shape
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
]


class Rock(NamedTuple):
    pieces: Tuple[Tuple[int, int], ...]

    def move(self, dx, dy) -> "Rock":
        return Rock(tuple((x + dx, y + dy) for x, y in self.pieces))

    def has_wall_collision(self, left, right):
        return not all(left < x < right for x, _ in self.pieces)

    def has_bottom_collision(self, bottom):
        return any(y <= bottom for _, y in self.pieces)

    def has_fallen_pieces_collision(self, fallen_pieces):
        return any(piece in fallen_pieces for piece in self.pieces)

    def has_any_collision(self, left, right, bottom, fallen_pieces):
        return self.has_wall_collision(left, right) \
               or self.has_bottom_collision(bottom) \
               or self.has_fallen_pieces_collision(fallen_pieces)


def debug(rock, fallen_pieces, move, top):
    print(move, top)
    top = max(y for _, y in rock.pieces)
    for y in range(top, -1, -1):
        print('|', end='')
        for x in range(0, 7):
            symbol = '.'
            if (x, y) in rock.pieces:
                symbol = '@'
            if (x, y) in fallen_pieces:
                symbol = '#'
            print(symbol, end='')
        print('|')
    print('+++++++++\n\n')


def find_bottom(fallen_pieces: Set[Tuple[int, int]], top: int, left, right):
    diffs = [(-1, 0), (1, 0), (0, -1)]
    visited = {}

    def dfs(x, y):
        if y < 0:
            return y

        if not (left < x < right):
            return float("inf")

        if (x, y) in fallen_pieces:
            return float("inf")

        if (x, y) in visited:
            return visited[(x, y)]

        visited[(x, y)] = float("inf")
        result = y
        for dx, dy in diffs:
            nx = x + dx
            ny = y + dy
            result = min(result, dfs(nx, ny))

        visited[(x, y)] = result
        return result

    return dfs(0, top)


def prune_v1(fallen_pieces: set, tops: list):
    threshold = min(tops)
    result = set()
    for node in fallen_pieces:
        if node[1] >= threshold:
            result.add(node)
    return result


def prune_v2(fallen_pieces: set, top):
    threshold = find_bottom(fallen_pieces, top, -1, 7)
    result = set()
    for node in fallen_pieces:
        if node[1] >= threshold:
            result.add(node)
    return result


def part_one(dirs, num=2022):
    fallen_pieces = set()
    top = -1

    shapes = cycle(SHAPES)
    moves = cycle(list(dirs))
    # start = time.time()

    for i in range(num):
        # if i % 1000 == 0:
        #     prev = len(fallen_pieces)
        #     # fallen_pieces = prune_v1(fallen_pieces, tops)
        #     fallen_pieces = prune_v2(fallen_pieces, top+3)
        #     if i % 1_000_000 == 0:
        #         print(i, prev, len(fallen_pieces), time.time() - start)
        #         start = time.time()

        rock = Rock(next(shapes)).move(2, top+4)

        for move in moves:
            if move == '<':
                dx = -1
            else:
                dx = 1

            nxt = rock.move(dx, 0)
            if not nxt.has_wall_collision(-1, 7) and not nxt.has_fallen_pieces_collision(fallen_pieces):
                rock = nxt
            # debug(rock, fallen_pieces, move, top)

            nxt = rock.move(0, -1)
            if nxt.has_bottom_collision(-1) or nxt.has_fallen_pieces_collision(fallen_pieces):
                break

            rock = nxt
            # debug(rock, fallen_pieces, '|', top)

        fallen_pieces.update(rock.pieces)
        for x, y in rock.pieces:
            top = max(top, y)
            # tops[x] = max(tops[x], y)
        # top = max(top, max(y for _, y in rock.pieces))
        # print(rock.pieces)
        # debug(rock, fallen_pieces, '-', top)

    print(len(fallen_pieces), top)
    return top + 1


def extend_history(history: list, top):
    if len(history) <= top:
        history.extend([[0] * 7 for _ in range(top - len(history) + 1)])


def apply_history(rock_numbers: dict, history: list, rock: Rock, rock_number: int):
    top = max(y for _, y in rock.pieces)
    extend_history(history, top)

    for x, y in rock.pieces:
        history[y][x] = 1
        rock_numbers[y] = rock_number


def find_pattern(history, rock_numbers, num):
    groups = defaultdict(list)

    for i, row in enumerate(history):
        key = tuple(row)

        for j in groups[key]:
            length = i - j
            if length < 20:
                continue
            if history[j:i] != history[i:i+length]:
                continue

            rock_in_interval = rock_numbers[i] - rock_numbers[j]
            rocks_leftover = num - rock_numbers[j]
            # print(i, j, rocks_leftover % rock_in_interval)
            if (num - rock_numbers[j]) % rock_in_interval > 1000:
                continue

            result = length * (rocks_leftover // rock_in_interval)
            print(j, i, length, rock_numbers[j], rock_numbers[i], rocks_leftover % rock_in_interval, length * (rocks_leftover // rock_in_interval))
            # other_side = rocks_leftover % rock_in_interval

            return result

        groups[key].append(i)

    return None


def part_two(dirs):
    num = 1_000_000_000_000
    print(len(dirs), len(dirs) % len(SHAPES), len(dirs) * len(SHAPES))
    history = []
    extend_history(history, 3)
    rock_numbers = {}
    fallen_pieces = set()
    top = -1

    shapes = cycle(SHAPES)
    moves = cycle(list(enumerate(dirs)))

    for rock_number in range(len(dirs) * len(SHAPES)):
        if rock_number % 10000 == 0:
            print(rock_number)
        #     if len(counter[tuple(history[0])]) > 4000:
        #         break
        rock = Rock(next(shapes)).move(2, top + 4)

        for move_num, move in moves:
            if move == '<':
                dx = -1
            else:
                dx = 1

            nxt = rock.move(dx, 0)
            if not nxt.has_wall_collision(-1, 7) and not nxt.has_fallen_pieces_collision(fallen_pieces):
                rock = nxt

            nxt = rock.move(0, -1)
            if nxt.has_bottom_collision(-1) or nxt.has_fallen_pieces_collision(fallen_pieces):
                break

            rock = nxt

        fallen_pieces.update(rock.pieces)
        top = max(top, max(y for _, y in rock.pieces))
        apply_history(rock_numbers, history, rock, rock_number)

    # print(len(fallen_pieces), top, sorted(counter[tuple(history[0])]))

    # candidates = sorted(counter[tuple(history[0])])[1:]
    # for candidate in candidates:
    #     length = candidate
    #     print(candidate, length, len(history[:length]), len(history[candidate:candidate+length]))
    #     if history[:length] == history[candidate:candidate+length]:
    #         print(candidate)
    #         return length
    # print("fail")

    # history = [[0]*7 for _ in range(top+1)]
    # for x, y in fallen_pieces:
    #     history[y][x] = 1

    return find_pattern(history, rock_numbers, num)

    # groups = defaultdict(set)
    # for y, row in enumerate(history):
    #     groups[tuple(row)].add(y)
    # print('groups number', len(groups))
    #
    # visited = set()
    # for i in range(len(dirs)):
    #     key = tuple(history[i])
    #     if key in visited:
    #         continue
    #     visited.add(key)
    #     candidates = sorted(groups[key])
    #     print(len(candidates))
    #     for candidate in candidates:
    #         if i == candidate:
    #             continue
    #         length = candidate - i
    #         if length <= len(dirs):
    #             continue
    #
    #         # print(len(dirs)*len(SHAPES))
    #         # if length % (len(dirs)*len(SHAPES)) != 0:
    #         #     continue
    #         # print(candidate, length, len(history[i:i+length]), len(history[candidate:candidate+length]))
    #         if history[i:i+length] == history[candidate:candidate+length]:
    #             rock_in_interval = rock_numbers[candidate] - rock_numbers[i]
    #             print(i, candidate, length, rock_numbers[i], rock_numbers[candidate], (num - rock_numbers[i]) % rock_in_interval)
    #             if (num - rock_numbers[i]) % rock_in_interval <= 1:
    #                 print(i, candidate, length, rock_numbers[i], rock_numbers[candidate])
    #                 print((num - rock_numbers[i]) % rock_in_interval)
    #                 rocks_leftover = num - rock_numbers[i]
    #                 result = length * (rocks_leftover // rock_in_interval) + i
    #                 return result
    #             # break
    #             # return length
    # return None


if __name__ == "__main__":
    # assert part_one(TEST) == 3068
    # assert part_one(open("input").read()) == 3130

    # assert part_two(TEST) == 1514285714288
    p1 = part_one(open("input").read(), 1600)
    print('part_one', p1)
    p2 = part_two(open("input").read())
    print(f"{p1=} {p2=} result {p1+p2}")
    print("DONE")
