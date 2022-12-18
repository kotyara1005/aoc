from collections import defaultdict

TEST = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

DIFFS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


class UF:
    def __init__(self):
        self.data = {}
        self.rank = {}

    def add(self, node):
        if node in self.data:
            return

        self.data[node] = node
        self.rank[node] = 0

    def find(self, node):
        if self.data[node] == node:
            return node

        self.data[node] = self.find(self.data[node])
        return self.data[node]

    def join(self, n1, n2):
        n1 = self.find(n1)
        n2 = self.find(n2)

        if n1 == n2:
            return

        if self.rank[n1] > self.rank[n2]:
            n1, n2 = n2, n1

        self.data[n1] = n2
        self.rank[n2] += self.rank[n1]


def parse_input(s: str):
    result = []
    for line in s.splitlines():
        result.append(tuple(map(int, line.split(','))))
    return result


def get_neighbors(x, y, z):
    for dx, dy, dz in DIFFS:
        yield (x+dx, y+dy, z+dz)


def part_one(cubes):
    surfaces = defaultdict(int)
    for cube in cubes:
        surfaces[cube] = 6
        for neighbor in get_neighbors(*cube):
            if neighbor in surfaces:
                surfaces[cube] -= 1
                surfaces[neighbor] -= 1

    return sum(surfaces.values())


def part_two(cubes):
    walls = set(cubes)
    min_x = min(x for x, y, z in cubes) - 2
    max_x = max(x for x, y, z in cubes) + 2
    min_y = min(y for x, y, z in cubes) - 2
    max_y = max(y for x, y, z in cubes) + 2
    min_z = min(z for x, y, z in cubes) - 2
    max_z = max(z for x, y, z in cubes) + 2


    def is_valid_cube(x, y, z):
        return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z

    uf = UF()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                node = (x, y, z)
                if node in walls:
                    continue
                uf.add(node)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                node = (x, y, z)
                if node in walls:
                    continue
                for neighbor in get_neighbors(*node):
                    if neighbor not in uf.data:
                        continue
                    uf.join(node, neighbor)

    outside_point = (min_x, min_y, min_z)
    outside_group = uf.find(outside_point)
    inside_bubbles = []

    for cube in uf.data:
        if uf.find(cube) != outside_group:
            inside_bubbles.append(cube)

    total_surface = part_one(cubes)
    inside_surface = part_one(inside_bubbles)

    return total_surface - inside_surface


if __name__ == '__main__':
    assert part_one(parse_input('1,1,1\n2,1,1')) == 10
    assert part_one(parse_input(TEST)) == 64
    print(part_one(parse_input(open("input").read())))

    assert part_two(parse_input(TEST)) == 58
    print(part_two(parse_input(open("input").read())))
    print("DONE")
