#!/usr/bin/env python3
from typing import List, Tuple, Dict, Set
from aocd import lines, submit
# from copy import deepcopy
from functools import reduce
from itertools import accumulate, chain
from operator import add
from collections import defaultdict
from queue import PriorityQueue

Map = List[List[int]]
Point = Tuple[int, int],


def parse(lines: List[str]) -> Map:
    return [[int(num) for num in line] for line in lines]


def index(point: Point, map: Map) -> int:
    return len(map[0]) * point[0] + point[1]


def point(index: int, map: Map) -> Point:
    return (index // len(map[0]), index % len(map[0]))


def combine_tuples(func, iterable1, iterable2):
    return tuple(map(func, iterable1, iterable2))


neighbour_offsets: List[Point] = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def dijkstra(map: Map) -> Tuple[List[int], List[int]]:
    predecessors: List[int] = [-1] * (len(map) * len(map[0]))
    distances: List[int] = [0] + [-1] * (len(map) * len(map[0]) - 1)
    queue: PriorityQueue = PriorityQueue()
    queue.put((0, 0))
    while not queue.empty():
        _, closest = queue.get()
        for neighbour_offset in neighbour_offsets:
            neighbour = combine_tuples(
                add, point(closest, map), neighbour_offset)
            if neighbour[0] < 0 or neighbour[0] == len(map) \
                    or neighbour[1] < 0 or neighbour[1] == len(map[0]):
                continue
            neighbour_index = index(neighbour, map)
            new_distance = distances[closest] + \
                map[neighbour[0]][neighbour[1]]
            if distances[neighbour_index] < 0 or distances[neighbour_index] > new_distance:
                distances[neighbour_index] = new_distance
                predecessors[neighbour_index] = closest
                queue.put((distances[neighbour_index], neighbour_index))
            assert(distances[neighbour_index] >= 0)
    return (predecessors, distances)


def part1(map: Map) -> int:
    _, distances = dijkstra(map)
    return distances[-1]


def elementwise(func, iterable):
    return list(map(func, iterable))


def increase_risk(val: int, amount: int) -> int:
    return (val + amount) % 10 + ((val + amount) // 10)


def part2(map: Map) -> int:
    def expand(row):
        return list(chain(row, *[elementwise(lambda x: increase_risk(x, i), row)
                                 for i in range(1, 5)]))
    map = [expand(row) for row in map]
    map = list(chain(map, *[[elementwise(lambda x: increase_risk(
        x, i), row) for row in map] for i in range(1, 5)]))
    # [print(row) for row in map]
    return part1(map)


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
    assert(part1(example_map) == 40)

    map = parse(lines)
    answer_a = part1(map)
    print(f"a {answer_a}")
    assert(answer_a == 609)
    # submit(answer_a, part="a")

    assert(part2(example_map) == 315)
    answer_b = part2(map)
    print(f"b {answer_b}")

    assert(answer_b == 2925)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
