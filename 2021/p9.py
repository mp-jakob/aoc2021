#!/usr/bin/env python3
from typing import List, Tuple, Dict
from aocd import lines, submit
import functools
from operator import add

Map = List[List[int]]


def parse(lines: List[str]) -> Map:
    return [[int(num) for num in line] for line in lines]


def elementwise(func, iterable1, iterable2):
    return list(map(func, iterable1, iterable2))


offsets: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def point_gradient(map: Map, point: Tuple[int, int]) -> int:
    height: int = sample(map, point)
    gradient = sum([sample(map, elementwise(add, point, offset))
                   > height for offset in offsets])
    return gradient


def pad_with(map: Map, padding: int) -> Map:
    return [[padding] * (len(map[0]) + 2)] + [[padding] + row + [padding]
                                              for row in map] + [[padding] * (len(map[0]) + 2)]


def sample(map: Map, point: Tuple[int, int]) -> int:
    return map[point[0]][point[1]]


def get_low_points(map: Map) -> Map:
    low_points: List[Tuple[int, int]] = []
    for y in range(1, len(map) - 1):
        for x in range(1, len(map[0]) - 1):
            if point_gradient(map, (y, x)) == 4:
                low_points.append((y, x))
    return low_points


def part1(map: Map) -> int:
    padded_map = pad_with(map, 10)
    low_points: List[Tuple[int, int]] = get_low_points(padded_map)
    risk_level: int = sum([sample(padded_map, point)
                          for point in low_points]) + len(low_points)
    return risk_level


# sufficient to check if one neighbour is basin
def fill(map: Map, basins: Map) -> Tuple[Map, Map]:
    delta: int = 1
    while delta > 0:
        delta = 0
        for y in range(1, len(map) - 1):
            for x in range(1, len(map[0]) - 1):
                point: Tuple[int, int] = (y, x)
                height: int = sample(map, point)
                is_basin: int = sample(basins, point)
                if not is_basin and height < 9:
                    floods: int = max(
                        [sample(basins, elementwise(add, point, offset)) for offset in offsets])
                    if floods:
                        delta += floods > 0
                        basins[y][x] = floods
    return (map, basins)


def create_map(dimensions: Tuple[int, int]) -> Map:
    # prevent shallow copy of rows
    # https://stackoverflow.com/a/13347704
    return [
        [0 for i in range(dimensions[1])]
        for i in range(dimensions[0])]


def part2(map: Map) -> int:
    padded_map = pad_with(map, 10)
    low_points: List[Tuple[int, int]] = get_low_points(padded_map)
    basins: Map = create_map([len(padded_map), len(padded_map[0])])
    for i, point in enumerate(low_points, start=1):
        basins[point[0]][point[1]] = i
    padded_map, basins = fill(padded_map, basins)
    basin_sizes: List[int] = [0] * (len(low_points) + 1)
    for row in basins:
        for x in row:
            basin_sizes[x] = basin_sizes[x] + 1

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
