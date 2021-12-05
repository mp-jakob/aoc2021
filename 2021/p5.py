#!/usr/bin/env python3
from typing import List, Tuple, Set
from aocd import lines
from aocd import submit
import functools
from parse import parse
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def parse_input(strings: List[str]) -> Tuple[List[Tuple[Point]], Point]:
    lines: List[Tuple[Point]] = []
    pattern = "{},{} -> {},{}"
    dimensions: Point = Point(0, 0)
    for line in strings:
        values = list(
            map(int, parse(pattern, line)))
        point1: Point = Point(values[0], values[1])
        point2: Point = Point(values[2], values[3])
        dimensions = Point(max([dimensions.x, point1.x, point2.x]),  max(
            [dimensions.y, point1.y, point2.y]))
        lines.append((point1, point2))

    return (lines, Point(dimensions.x + 1, dimensions.y + 1))


def create_map(dimensions: Point) -> List[List[int]]:
    # prevent shallow copy of rows
    # https://stackoverflow.com/a/13347704
    return [
        [0 for i in range(dimensions.x)]
        for i in range(dimensions.y)]


def count_overlaps(map: List[List[int]]) -> int:
    def row_summator(accumulator, val): return accumulator + \
        1 if val >= 2 else accumulator
    return sum([functools.reduce(row_summator, row, 0) for row in map])


def part1(lines: List[Tuple[Point, Point]], dimensions: Point) -> int:
    map = create_map(dimensions)
    for start, end in lines:
        if start.x == end.x:
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                map[y][start.x] += 1
        if start.y == end.y:
            for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                map[start.y][x] += 1
    return count_overlaps(map)


def part2(lines: List[Tuple[Point, Point]], dimensions: Point) -> int:
    map = create_map(dimensions)
    for start, end in lines:
        diff = (abs(end.x-start.x), abs(end.y-start.y))
        if diff[0] > diff[1]:
            if start.x > end.x:
                start, end = end, start
            direction: int = 0
            if end.y > start.y:
                direction = 1
            elif end.y < start.y:
                direction = -1
            y = start.y
            for x in range(start.x, end.x + 1):
                map[y][x] += 1
                y += direction
        else:
            if start.y > end.y:
                start, end = end, start
            direction: int = 0
            if end.x > start.x:
                direction = 1
            elif end.x < start.x:
                direction = -1
            x = start.x
            for y in range(start.y, end.y + 1):
                map[y][x] += 1
                x += direction
    # for row in map:
    #     print(row)
    return count_overlaps(map)


def main():
    example: List[str] = [
        "0, 9 -> 5, 9",
        "8, 0 -> 0, 8",
        "9, 4 -> 3, 4",
        "2, 2 -> 2, 1",
        "7, 0 -> 7, 4",
        "6, 4 -> 2, 0",
        "0, 9 -> 2, 9",
        "3, 4 -> 1, 4",
        "0, 0 -> 8, 8",
        "5, 5 -> 8, 2",
    ]

    example_lines, example_dimensions = parse_input(example)
    print(example_lines)
    print(example_dimensions)
    assert(part1(example_lines, example_dimensions) == 5)

    i_lines, dimensions = parse_input(lines)
    answer_a = part1(i_lines, dimensions)

    print(f"a {answer_a}")
    assert(answer_a == 7674)
    # submit(answer_a, part="a")

    assert(part2(example_lines, example_dimensions) == 12)
    answer_b = part2(i_lines, dimensions)

    print(f"b {answer_b}")
    assert(answer_b == 20898)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
