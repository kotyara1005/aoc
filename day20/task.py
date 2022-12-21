from dataclasses import dataclass

TEST = """\
1
2
-3
3
-2
0
4"""


def parse_input(s: str) -> list[int]:
    return list(map(int, s.splitlines()))


@dataclass
class Node:
    next: "Node"
    prev: "Node"
    index: int
    step: int

    def __eq__(self, other):
        return self.index == other.index


@dataclass
class DList:
    head: Node
    tail: Node


def create_dl():
    head = Node(None, None, -1, 0)
    tail = Node(None, None, -2, 0)
    head.next = head.prev = tail
    tail.next = tail.prev = head

    return DList(head, tail)


def append(dl: DList, index, step):
    prev = dl.tail.prev
    node = Node(dl.tail, prev, index, step)
    prev.next = node
    dl.tail.prev = node

    return node


def print_dl(dl: DList):
    cur = dl.head.next
    r = []
    while cur != dl.tail:
        r.append(cur.step)
        cur = cur.next
    print(r, len(r))


def pop_node(node):
    prev = node.prev
    nxt = node.next

    prev.next = nxt
    nxt.prev = prev


def insert_after(prev: Node, node: Node):
    nxt = prev.next
    prev.next = node
    nxt.prev = node
    node.prev = prev
    node.next = nxt


def mix(nums, dl, index):
    # print_dl(dl)
    for i, num in enumerate(nums):
        # print_dl(dl)
        node = index[i]
        pop_node(node)
        step = node.step % (len(nums)-1)

        cur = node.prev
        for _ in range(step):
            cur = cur.next
            if cur == dl.tail:
                cur = cur.next.next
        insert_after(cur, node)
        # print_dl(dl)
        # print(step, num, num % len(nums))

    # print_dl(dl)


def find_result(nums, dl):
    result = 0
    cur = dl.head.next
    while cur.step != 0:
        cur = cur.next

    id1 = (1000 % len(nums))
    id2 = (2000 % len(nums))
    id3 = (3000 % len(nums))
    print(id1, id2, id3)
    i = 0
    c = 0
    while c < 3:
        if i == id1:
            result += cur.step
            c += 1
            print(i, cur.step)
        if i == id2:
            result += cur.step
            c += 1
            print(i, cur.step)
        if i == id3:
            result += cur.step
            c += 1
            print(i, cur.step)

        i += 1
        cur = cur.next
        if cur == dl.tail:
            cur = cur.next.next

    print(result)
    return result


def part_one(nums: list[int]):
    index = {}
    dl = create_dl()
    for i, num in enumerate(nums):
        index[i] = append(dl, i, num)

    mix(nums, dl, index)
    return find_result(nums, dl)


def part_two(nums: list[int]):
    nums = [num * 811589153 for num in nums]
    index = {}
    dl = create_dl()
    for i, num in enumerate(nums):
        index[i] = append(dl, i, num)

    for _ in range(10):
        mix(nums, dl, index)
    return find_result(nums, dl)


if __name__ == '__main__':
    assert part_one(parse_input(TEST)) == 3
    print(part_one(parse_input(open("input").read())))

    assert part_two(parse_input(TEST)) == 1623178306
    print(part_two(parse_input(open("input").read())))
    print("DONE")
