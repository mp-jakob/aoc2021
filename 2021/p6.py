#!/usr/bin/env python3
from typing import Iterable, List, Tuple, Set
from aocd import lines
from aocd import submit
from collections import Counter


def parse(lines: List[str]) -> List[int]:
    return [int(number) for number in lines[0].split(",")]


def part1(input: List[int], days: int = 80) -> int:
    fishes = [0] * 9
    count = Counter(input)
    for i in range(9):
        fishes[i] = count[i]
    for day in range(days):
        spawns: int = fishes[0]
        fishes = fishes[1:] + [spawns]
        fishes[6] += spawns
    return sum(fishes)


def main():
    example: List[str] = ["3, 4, 3, 1, 2"]

    example_fishes = parse(example)
    assert(part1(example_fishes) == 5934)

    fishes = parse(lines)
    answer_a = part1(fishes)

    print(f"a {answer_a}")
    assert(answer_a == 380758)
    # submit(answer_a, part="a")

    assert(part1(example_fishes, 256) == 26984457539)
    answer_b = part1(fishes, 256)

    print(f"b {answer_b}")
    assert(answer_b == 1710623015163)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
