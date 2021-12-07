#!/usr/bin/env python3
from typing import Iterable, List, Tuple, Set
from aocd import lines
from aocd import submit
from operator import add
import functools


def parse(lines: List[str]) -> List[int]:
    return [int(number) for number in lines[0].split(",")]


def elementwise(func, iterable):
    return list(map(func, iterable))


def dist(a: int, b: int) -> int:
    return abs(a - b)


def part1(crabs: List[int]) -> int:
    costs: List[int] = [sum(elementwise(
        lambda x: dist(x, position), crabs)) for position in range(max(crabs) + 1)]
    return min(costs)


def part2(crabs: List[int]) -> int:
    def arith_sum(x, y): return ((dist(x, y) + 1) * dist(x, y) // 2)
    costs: List[int] = [sum(elementwise(
        lambda x: arith_sum(x, position), crabs)) for position in range(max(crabs) + 1)]
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
