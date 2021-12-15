#!/usr/bin/env python3
from typing import List, Tuple, Dict, Set
from aocd import lines, submit
# from copy import deepcopy
# from functools import reduce
from itertools import accumulate
from operator import add


Map = List[List[int]]
Point = Tuple[int, int],


def parse(lines: List[str]) -> Map:
    return [[int(num) for num in line] for line in lines]


def index(point: Point, map: Map) -> int:
    return len(map[0]) * point[0] + point[1]


def point(index: int, map: Map) -> Point:
    return (index // len(map[0]), index % len(map[0]))


def combine_tuples(func, iterable1, iterable2):
    return list(map(func, iterable1, iterable2))


neighbour_offsets: List[Point] = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def part1(map: Map) -> int:
    predecessors: List[int] = [-1] * (len(map) * len(map[0]))
    distances: List[int] = [0] + [-1] * (len(map) * len(map[0]) - 1)
    unvisited: Set[int] = set(range(len(predecessors)))
    while unvisited:
        def min_dist(x, y): return x if distances[x] < distances[y] else y
        closest = next(accumulate(unvisited, min_dist))
        unvisited.remove(closest)
        for neighbour_offset in neighbour_offsets:
            neighbour = combine_tuples(
                add, point(closest, map), neighbour_offset)
            if neighbour[0] < 0 or neighbour[0] >= len(map) \
                    or neighbour[1] < 0 or neighbour[1] >= len(map[0]):
                continue
            neighbour_index = index(neighbour, map)
            print(neighbour)
            new_distance = distances[closest] + \
                map[neighbour[0]][neighbour[1]]
            if distances[neighbour_index] < 0 or distances[neighbour_index] > new_distance:
                distances[neighbour_index] = new_distance
                predecessors[neighbour_index] = closest

    curr = len(distances) - 1
    cost = 0
    while curr != 0:
        curr_point = point(curr, map)
        # print(curr_point)
        cost += map[curr_point[0]][curr_point[1]]
        curr = predecessors[curr]

    return cost


def main():
    example: List[str] = [
        "1163751742",
        "1381373672",
        "2136511328",
        "3694931569",
        "7463417111",
        "1319128137",
        "1359912421",
        "3125421639",
        "1293138521",
        "2311944581",

    ]

    example_map = parse(example)
    assert(part1(example_map, ) == 40)

    map = parse(lines)
    answer_a = part1(map)
    print(f"a {answer_a}")
    assert(answer_a == 609)
    submit(answer_a, part="a")

    # assert(part1(example_map, example_insertions, 40) == 2188189693529)
    # answer_b = part1(template, inserrions, 40)
    # print(f"b {answer_b}")

    # assert(answer_b == 2926813379532)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
