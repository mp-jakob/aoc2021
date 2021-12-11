#!/usr/bin/env python3
from typing import List, Tuple
from aocd import lines, submit
import itertools
from copy import deepcopy
from operator import countOf
Map = List[List[int]]


def parse(lines: List[str]) -> Map:
    return [[int(num) for num in line] for line in lines]


offsets: List[Tuple[int, int]] = [
    (-1, 0), (1, 0),
    (0, -1), (0, 1),
    (1, 1), (1, -1),
    (-1, 1), (-1, -1)
]


def coordinate_range(map: Map):
    return itertools.product(range(len(map)), range(len(map[0])))


def iteration(map: Map) -> int:
    # map = [[x + 1 for x in row] for row in map]
    for coord in coordinate_range(map):
        map[coord[0]][coord[1]] += 1

    worklist = list(coordinate_range(map))
    while len(worklist):
        coord, *worklist = worklist
        if map[coord[0]][coord[1]] == 0:
            continue
        elif map[coord[0]][coord[1]] > 9:
            map[coord[0]][coord[1]] = 0
            neighbours = [(coord[0] + offset[0], coord[1] + offset[1])
                          for offset in offsets]
            neighbours = filter(lambda point: 0 <= point[0] < len(
                map) and 0 <= point[1] < len(map[0]), neighbours)
            not_flashed = filter(
                lambda point: map[point[0]][point[1]] > 0, neighbours)
            for neighbour in not_flashed:
                map[neighbour[0]][neighbour[1]] += 1
                worklist.append(neighbour)

    flashes = countOf(itertools.chain(*map), 0)
    return flashes


def part1(map: Map, iterations: int) -> int:
    map = deepcopy(map)
    flashes: int = 0
    for i in range(iterations):
        flashes += iteration(map)
    return flashes


def part2(map: Map) -> int:
    map = deepcopy(map)
    flashes: int = 0
    iterations: int = 0
    while flashes < len(map) * len(map[0]):
        iterations += 1
        flashes = iteration(map)

    return iterations


def main():
    example: List[str] = [
        "5483143223",
        "2745854711",
        "5264556173",
        "6141336146",
        "6357385478",
        "4167524645",
        "2176841721",
        "6882881134",
        "4846848554",
        "5283751526",
    ]

    example_octopuses = parse(example)
    assert(part1(example_octopuses, 2) == 35)
    assert(part1(example_octopuses, 3) == 35 + 45)
    assert(part1(example_octopuses, 10) == 204)
    assert(part1(example_octopuses, 100) == 1656)

    octopuses = parse(lines)
    answer_a = part1(octopuses, 100)
    print(f"a {answer_a}")
    assert(answer_a == 1625)
    # submit(answer_a, part="a")

    assert(part2(example_octopuses) == 195)

    answer_b = part2(octopuses)
    print(f"b {answer_b}")
    assert(answer_b == 244)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
