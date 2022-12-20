import re, time
from typing import NamedTuple
from functools import cache
from contextlib import ContextDecorator


class TimeIt(ContextDecorator):
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(time.time() - self.start)
        return True


TEST = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

REGEX = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian\.")




class RobotCost(NamedTuple):
    ore: int
    clay: int
    obsidian: int


class Supply(NamedTuple):
    ore: int
    clay: int
    obsidian: int

    def __add__(self, other):
        return Supply(*[a+b for a,b in zip(self, other)])


class Limits(NamedTuple):
    ore_robots: int
    clay_robots: int
    obsidian_robots: int

    def apply(self, supply: Supply):
        return Supply(
            ore=min(supply.ore, self.ore_robots * 2),
            clay=min(supply.clay, self.clay_robots * 2),
            obsidian=min(supply.obsidian, self.obsidian_robots * 2),
        )


class Blueprint(NamedTuple):
    id: int
    ore_robot_cost: RobotCost
    clay_robot_cost: RobotCost
    obsidian_robot_cost: RobotCost
    geode_robot_cost: RobotCost

    limits: Limits


class Fleet(NamedTuple):
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int

    def mine(self) -> (Supply, int):
        return (
            Supply(
                self.ore_robots,
                self.clay_robots,
                self.obsidian_robots,
            ),
            self.geode_robots,
        )


def get_max_number_of_robots(cost: RobotCost, supply: Supply):
    numbers = []
    if cost.ore:
        numbers.append(supply.ore // cost.ore)

    if cost.clay:
        numbers.append(supply.clay // cost.clay)

    if cost.obsidian:
        numbers.append((supply.obsidian // cost.obsidian))

    return min(numbers)


def can_produce(cost: RobotCost, supply: Supply) -> bool:
    return all(a >= b for a, b in zip(supply, cost))


def produce_robots(cost: RobotCost, supply: Supply, number) -> Supply:
    return Supply(
        ore=supply.ore - cost.ore * number,
        clay=supply.clay - cost.clay * number,
        obsidian=supply.obsidian - cost.obsidian * number,
    )


def can_make_all(bl: Blueprint, supply: Supply):
    ore = sum(
        [bl.ore_robot_cost.ore,
        bl.clay_robot_cost.ore,
        bl.obsidian_robot_cost.ore,
        bl.geode_robot_cost.ore,]
    )
    clay = sum(
        [bl.ore_robot_cost.clay,
        bl.clay_robot_cost.clay,
        bl.obsidian_robot_cost.clay,
        bl.geode_robot_cost.clay,]
    )
    obsidian = sum(
        [bl.ore_robot_cost.obsidian,
        bl.clay_robot_cost.obsidian,
        bl.obsidian_robot_cost.obsidian,
        bl.geode_robot_cost.obsidian,]
    )

    return supply.ore >= ore and supply.clay >= clay and supply.obsidian >= obsidian


def parse_input(s: str):
    result = []
    for line in s.splitlines():
        _id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = map(int, REGEX.match(line).groups())
        bl = Blueprint(
            _id,
            RobotCost(ore_ore, 0, 0),
            RobotCost(clay_ore, 0, 0),
            RobotCost(obsidian_ore, obsidian_clay, 0),
            RobotCost(geode_ore, 0, geode_obsidian),
            Limits(
                ore_robots=max(0, ore_ore, clay_ore, obsidian_ore, geode_ore),
                clay_robots=obsidian_clay,
                obsidian_robots=geode_obsidian,
            )
        )
        result.append(bl)
    return result


@TimeIt()
def part_one(blueprints: list[Blueprint]):
    result = 0
    for bl in blueprints:
        result += check_blueprint(bl, 24) * bl.id

    return result


@TimeIt()
def part_two(blueprints: list[Blueprint]):
    result = 1
    for bl in blueprints[:3]:
        result *= check_blueprint(bl, 32)

    return result



@TimeIt()
def check_blueprint(blueprint: Blueprint, t) -> int:
    stack = []

    @cache
    def dp(
            time: int,
            prev_geodes: int,
            robots: Fleet,
            supply: Supply
    ) -> int:
        # print(time, prev_geodes, robots, supply)
        if time == 0:
            # if prev_geodes >= 9:
            #     stack.append((robots, supply))
            #     for i, r in enumerate(stack):
            #         print(i, *r)
            #     print(prev_geodes, '\n\n')
            #     stack.pop()
            return prev_geodes

        mined_supply, new_geodes = robots.mine()

        result = prev_geodes

        if can_produce(blueprint.geode_robot_cost, supply):
            loc = dp(
                time - 1,
                prev_geodes + new_geodes,
                Fleet(
                    robots.ore_robots,
                    robots.clay_robots,
                    robots.obsidian_robots,
                    robots.geode_robots + 1,
                ),
                blueprint.limits.apply(produce_robots(blueprint.geode_robot_cost, supply, 1) + mined_supply),
            )
            result = max(result, loc)
        else:
            if can_produce(blueprint.ore_robot_cost, supply) and blueprint.limits.ore_robots > robots.ore_robots:
                loc = dp(
                    time - 1,
                    prev_geodes + new_geodes,
                    Fleet(
                        robots.ore_robots + 1,
                        robots.clay_robots,
                        robots.obsidian_robots,
                        robots.geode_robots,
                    ),
                    blueprint.limits.apply(produce_robots(blueprint.ore_robot_cost, supply, 1) + mined_supply),
                )
                result = max(result, loc)

            if can_produce(blueprint.clay_robot_cost, supply) and blueprint.limits.clay_robots > robots.clay_robots:
                loc = dp(
                    time - 1,
                    prev_geodes + new_geodes,
                    Fleet(
                        robots.ore_robots,
                        robots.clay_robots + 1,
                        robots.obsidian_robots,
                        robots.geode_robots,
                    ),
                    blueprint.limits.apply(produce_robots(blueprint.clay_robot_cost, supply, 1) + mined_supply),
                )
                result = max(result, loc)

            if can_produce(blueprint.obsidian_robot_cost, supply) and blueprint.limits.obsidian_robots > robots.obsidian_robots:
                loc = dp(
                    time - 1,
                    prev_geodes + new_geodes,
                    Fleet(
                        robots.ore_robots,
                        robots.clay_robots,
                        robots.obsidian_robots + 1,
                        robots.geode_robots,
                    ),
                    blueprint.limits.apply(produce_robots(blueprint.obsidian_robot_cost, supply, 1) + mined_supply),
                )
                result = max(result, loc)

            loc = dp(
                time - 1,
                prev_geodes + new_geodes,
                Fleet(
                    robots.ore_robots,
                    robots.clay_robots,
                    robots.obsidian_robots,
                    robots.geode_robots,
                ),
                blueprint.limits.apply(supply + mined_supply),
            )
            result = max(result, loc)

        return result

        # geode_num = get_max_number_of_robots(blueprint.geode_robot_cost, supply)
        # if geode_num:
        #     supply = produce_robots(blueprint.geode_robot_cost, supply, 1)
        #
        # max_ore_num = min(
        #     get_max_number_of_robots(blueprint.ore_robot_cost, supply),
        #     blueprint.limits.ore_robots - robots.ore_robots,
        # )
        #
        # for ore_num in range(max_ore_num + 1):
        #     supply1 = produce_robots(blueprint.ore_robot_cost, supply, ore_num)
        #     max_clay_num = min(
        #         get_max_number_of_robots(blueprint.clay_robot_cost, supply1),
        #         blueprint.limits.clay_robots - robots.clay_robots,
        #     )
        #     for clay_num in range(max_clay_num + 1):
        #         supply2 = produce_robots(blueprint.clay_robot_cost, supply1, clay_num)
        #         max_obsidian_num = min(
        #             get_max_number_of_robots(blueprint.obsidian_robot_cost, supply2),
        #             blueprint.limits.obsidian_robots - robots.obsidian_robots,
        #         )
        #         for obsidian_num in range(max_obsidian_num + 1):
        #             supply3 = produce_robots(blueprint.obsidian_robot_cost, supply2, obsidian_num)
        #             stack.append((robots, supply))
        #             loc = dp(
        #                 time - 1,
        #                 prev_geodes + new_geodes,
        #                 Fleet(
        #                     robots.ore_robots + ore_num,
        #                     robots.clay_robots + clay_num,
        #                     robots.obsidian_robots + obsidian_num,
        #                     robots.geode_robots + geode_num,
        #                 ),
        #                 blueprint.limits.apply(supply3 + mined_supply),
        #             )
        #             result = max(result, loc)
        #             stack.pop()

        # return result

    rv = dp(t, 0, Fleet(1, 0, 0, 0), Supply(0, 0, 0))
    print(blueprint.id, rv)
    return rv


if __name__ == '__main__':
    bls = parse_input(TEST)
    # assert check_blueprint(bls[0], 24) == 9
    # assert check_blueprint(bls[1], 24) == 12
    # assert part_one(bls) == 33
    # print("part_one", part_one(parse_input(open("input").read())))

    assert part_two(bls) == 56*62
    print("part_two", part_two(parse_input(open("input").read())))

    print("DONE")
