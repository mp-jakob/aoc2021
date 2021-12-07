#!/usr/bin/env python3
from typing import List
from aocd import lines, submit
import functools


def parse(lines: List[str]) -> List[int]:
    return [int(number) for number in lines[0].split(",")]


def dist(a: int, b: int) -> int:
    return abs(a - b)


def part1(crabs: List[int]) -> int:
    costs: List[int] = [
        functools.reduce(lambda sum, crab: sum +
                         dist(crab, position), crabs, 0)
        for position in range(max(crabs) + 1)]
    return min(costs)


def gaussian_sum(n: int):
    return ((n + 1) * n // 2)


def part2(crabs: List[int]) -> int:
    costs: List[int] = [
        functools.reduce(lambda sum, crab: sum +
                         gaussian_sum(dist(crab, position)), crabs, 0)
        for position in range(max(crabs) + 1)]
    return min(costs)


def main():
    example: List[str] = ["16,1,2,0,4,2,7,1,2,14"]

    example_crabs = parse(example)
    assert(part1(example_crabs) == 37)

    crabs = parse(lines)

    answer_a = part1(crabs)
    print(f"a {answer_a}")
    assert(answer_a == 326132)
    # submit(answer_a, part="a")

    assert(part2(example_crabs) == 168)

    answer_b = part2(crabs)
    print(f"b {answer_b}")
    assert(answer_b == 88612508)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
