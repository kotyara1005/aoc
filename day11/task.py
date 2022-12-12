from dataclasses import dataclass
from typing import Callable
import operator

TEST = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


"""
Monkey 0:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by 19 to 1501.
    Monkey gets bored with item. Worry level is divided by 3 to 500.
    Current worry level is not divisible by 23.
    Item with worry level 500 is thrown to monkey 3.
"""

OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.mod,
}


@dataclass
class Monkey:
    id: int
    items: list
    operation: Callable
    attr1: str
    attr2: str
    divisor: int
    if_true: int
    if_false: int
    inspected_items: int

    def apply_operation(self, worry):
        if self.attr1.isnumeric():
            a = int(self.attr1)
        else:
            a = worry

        if self.attr2.isnumeric():
            b = int(self.attr2)
        else:
            b = worry

        # if a == b == worry:
        #     return worry

        return self.operation(a, b)


def parse_input(text: str):
    monkeys = []

    for monkey in text.split("\n\n"):
        monkey = monkey.splitlines()
        ops = monkey[2][19:].split()
        monkeys.append(Monkey(
            id=int(monkey[0][7:-1]),
            items=list(map(int, monkey[1][18:].split(", "))),
            operation=OPERATIONS[ops[1]],
            attr1=ops[0],
            attr2=ops[2],
            divisor=int(monkey[3].split(" ")[-1]),
            if_true=int(monkey[4].split(" ")[-1]),
            if_false=int(monkey[5].split(" ")[-1]),
            inspected_items=0,
        ))

    return monkeys


def simulation(monkeys: list[Monkey], number_of_rounds, divisor):
    max_val = 1
    for m in monkeys:
        max_val = max_val * m.divisor
    # print(r)
    # print([m.divisor for m in monkeys])
    # return
    for r in range(number_of_rounds):
        if r % 100 == 0:
            print(r)
            print([m.inspected_items for m in monkeys])
            # print([max(m.items, default=-1) for m in monkeys])
        for monkey in monkeys:
            while monkey.items:
                worry = monkey.apply_operation(monkey.items.pop())
                if divisor is not None:
                    worry = worry // divisor
                worry = worry % max_val
                if worry % monkey.divisor == 0:
                    monkeys[monkey.if_true].items.append(worry)
                else:
                    monkeys[monkey.if_false].items.append(worry)
                monkey.inspected_items += 1
    print([m.inspected_items for m in monkeys])
    print(operator.mul(*sorted(m.inspected_items for m in monkeys)[-2:]))
    return operator.mul(*sorted(m.inspected_items for m in monkeys)[-2:])

# 14170964332
# 14178012075


if __name__ == '__main__':
    # print(parse_input(TEST))
    assert simulation(parse_input(TEST), 20, 3) == 10605
    print(simulation(parse_input(open("input").read()), 20, 3))

    assert simulation(parse_input(TEST), 10000, None) == 2713310158
    print(simulation(parse_input(open("input").read()), 10000, None))
