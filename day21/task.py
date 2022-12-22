import operator

TEST = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

IN_PROCESS = object()
OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.itruediv,
}


def parse_input(s: str):
    graph = {}

    for line in s.splitlines():
        monkey, val = line.split(": ")
        if val.isnumeric():
            graph[monkey] = {"val": int(val)}
        else:
            left, op, right = val.split(" ")
            graph[monkey] = {"left": left, "right": right, "op": OPERATIONS[op]}

    return graph


def part_one(graph: dict) -> int:
    visited = {name: node["val"] for name, node in graph.items() if "val" in node}

    def dfs(node):
        if visited.get(node) is IN_PROCESS:
            raise Exception("cycle")

        if node in visited:
            return visited[node]
        visited[node] = IN_PROCESS
        visited[node] = graph[node]["op"](dfs(graph[node]["left"]), dfs(graph[node]["right"]))
        return visited[node]

    rv = dfs("root")
    print(rv)
    return rv


def part_two(graph: dict, operation):
    assert check_degree(graph) == 1, "It's linear function"
    # So now we can apply binary search

    left, right = 0, 2_000_000_000_000_000
    while left < right:
        mid = (left + right) // 2
        rv = check_result(graph, mid, operation)
        if rv is None:
            print(mid)
            return mid

        if rv:
            left = mid
        else:
            right = mid

    # print(rv, visited[graph["root"]["left"]], visited[graph["root"]["right"]])
    # return rv


def check_degree(graph):
    prev_op = graph["root"]["op"]
    prev = graph["humn"]["val"]
    graph["root"]["op"] = operator.eq
    graph["humn"]["val"] = float("inf")
    visited = {name: int(name == "humn") for name, node in graph.items() if "val" in node}

    def dfs(node):
        if visited.get(node) is IN_PROCESS:
            raise Exception("cycle")

        if node in visited:
            return visited[node]
        visited[node] = IN_PROCESS
        if graph[node]["op"] is operator.mul:
            visited[node] = dfs(graph[node]["left"]) + dfs(graph[node]["right"])
        else:
            visited[node] = max(dfs(graph[node]["left"]), dfs(graph[node]["right"]))
        return visited[node]

    result = dfs("root")
    graph["humn"]["val"] = prev
    graph["root"]["op"] = prev_op
    return result


def check_result(graph, guess, operation):
    graph["root"]["op"] = operation
    graph["humn"]["val"] = guess
    visited = {name: node["val"] for name, node in graph.items() if "val" in node}

    def dfs(node):
        if visited.get(node) is IN_PROCESS:
            raise Exception("cycle")

        if node in visited:
            return visited[node]
        visited[node] = IN_PROCESS
        visited[node] = graph[node]["op"](dfs(graph[node]["left"]), dfs(graph[node]["right"]))
        return visited[node]

    result = dfs("root")
    if visited[graph["root"]["left"]] == visited[graph["root"]["right"]]:
        return None
    return result


if __name__ == '__main__':
    assert part_one(parse_input(TEST)) == 152
    print(part_one(parse_input(open("input").read())))

    print(check_result(parse_input(TEST), 0, operator.lt))
    print(check_result(parse_input(TEST), 2_000_000, operator.lt))
    print(check_result(parse_input(TEST), 2_000_000_000, operator.lt))
    print(check_result(parse_input(TEST), 282_285_213_953_670, operator.lt))
    assert part_two(parse_input(TEST), operator.lt) == 301

    print(check_result(parse_input(open("input").read()), 0, operator.gt))
    print(check_result(parse_input(open("input").read()), 2_000_000, operator.gt))
    print(check_result(parse_input(open("input").read()), 2_000_000_000, operator.gt))
    print(check_result(parse_input(open("input").read()), 282_285_213_953_670, operator.gt))
    print(part_two(parse_input(open("input").read()), operator.gt))
    print("DONE")
