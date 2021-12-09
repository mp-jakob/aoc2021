#!/usr/bin/env python3
from typing import List, Tuple, Dict
from aocd import lines, submit
import functools
import itertools
from operator import add

Map = List[List[int]]


def parse(lines: List[str]) -> Map:
    return [[int(num) for num in line] for line in lines]


def elementwise(func, iterable1, iterable2):
    return list(map(func, iterable1, iterable2))


offsets: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def pad_with(map: Map, padding: int) -> Map:
    return [[padding] * (len(map[0]) + 2)] + \
        [[padding] + row + [padding] for row in map] + \
        [[padding] * (len(map[0]) + 2)]


def sample(map: Map, point: Tuple[int, int]) -> int:
    return map[point[0]][point[1]]


def is_low_point(map: Map, point: Tuple[int, int]) -> int:
    height: int = sample(map, point)
    return all([sample(map, elementwise(add, point, offset))
                > height for offset in offsets])


def get_low_points(map: Map) -> Map:
    return list(filter(lambda x: is_low_point(map, x), itertools.product(
        range(1, len(map) - 1), range(1, len(map[0]) - 1))))


def part1(height_map: Map) -> int:
    padded_map = pad_with(height_map, 10)
    low_points = get_low_points(padded_map)
    low_point_heights = map(lambda point: sample(
        padded_map, point), low_points)
    risk_level: int = functools.reduce(
        add, low_point_heights, 0) + len(low_points)
    return risk_level


# use while rather than recursion to not kill stack
def fill(height_map: Map, basin_map: Map) -> Map:
    delta: bool = True
    while delta:
        delta = False
        coordinates = itertools.product(
            range(1, len(height_map) - 1), range(1, len(height_map[0]) - 1))
        non_basin = filter(lambda coord: not sample(
            basin_map, coord), coordinates)
        non_top = filter(lambda coord: sample(
            height_map, coord) < 9, non_basin)
        for coordinate in non_top:
            neighbour_basins = map(lambda offset: sample(
                basin_map, elementwise(add, coordinate, offset)), offsets)
            flooding_basin: int = next(
                filter(lambda x: x > 0, neighbour_basins), 0)
            delta |= flooding_basin > 0
            basin_map[coordinate[0]][coordinate[1]] = flooding_basin
    return basin_map


def create_map(dimensions: Tuple[int, int]) -> Map:
    # prevent shallow copy of rows
    # https://stackoverflow.com/a/13347704
    return [
        [0 for i in range(dimensions[1])]
        for i in range(dimensions[0])]


def part2(map: Map) -> int:
    padded_map = pad_with(map, 10)
    low_points: List[Tuple[int, int]] = get_low_points(padded_map)
    basin_map: Map = create_map([len(padded_map), len(padded_map[0])])
    for i, point in enumerate(low_points, start=1):
        basin_map[point[0]][point[1]] = i
    basin_map = fill(padded_map, basin_map)

    basin_sizes: List[int] = [0] * (len(low_points) + 1)
    # https://docs.python.org/3/library/itertools.html#itertools.chain
    for cell in itertools.chain(*basin_map):
        basin_sizes[cell] += 1

    highest_three = sorted(basin_sizes[1:], reverse=True)[0:3]
    return functools.reduce(lambda x, y: x * y, highest_three, 1)


def main():
    example: List[str] = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]

    example_map = parse(example)
    assert(part1(example_map) == 15)

    map = parse(lines)

    answer_a = part1(map)
    print(f"a {answer_a}")
    assert(answer_a == 580)
    # submit(answer_a, part="a")

    assert(part2(example_map) == 1134)

    answer_b = part2(map)
    print(f"b {answer_b}")
    assert(answer_b == 856716)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
