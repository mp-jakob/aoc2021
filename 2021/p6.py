#!/usr/bin/env python3
from typing import Iterable, List, Tuple, Set
from aocd import lines
from aocd import submit
from operator import add


def parse(lines: List[str]) -> List[int]:
    return [int(number) for number in lines[0].split(",")]


def elementwise(func, iterable1, iterable2):
    return list(map(func, iterable1, iterable2))


# as functional as it can get without overflowing the stack
def solution(input: List[int], days: int) -> int:
    fishes: List[int] = [input.count(i) for i in range(9)]
    for _ in range(days):
        # cyclic left shift, append spawns of spawning fishes
        fishes = fishes[1:] + [fishes[0]]
        # increase lifetime 6 with number of fishes that spawned
        fishes = elementwise(add, fishes, [0, 0, 0, 0, 0, 0, fishes[8], 0, 0])
    return sum(fishes)


def main():
    example: List[str] = ["3, 4, 3, 1, 2"]

    example_fishes = parse(example)
    assert(solution(example_fishes, 80) == 5934)

    fishes = parse(lines)
    answer_a = solution(fishes, 80)

    print(f"a {answer_a}")
    assert(answer_a == 380758)
    # submit(answer_a, part="a")

    assert(solution(example_fishes, 256) == 26984457539)
    answer_b = solution(fishes, 256)

    print(f"b {answer_b}")
    assert(answer_b == 1710623015163)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
