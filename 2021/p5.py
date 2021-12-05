#!/usr/bin/env python3
from typing import Iterable, List, Tuple, Set
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
    non_diagonal = filter(
        lambda line: line[0].x == line[1].x or line[0].y == line[1].y, lines)
    return part2(non_diagonal, dimensions)


def sign(num: int) -> int:
    return num // max(abs(num), 1)


def combine(func, iterable1, iterable2):
    return list(map(func, iterable1, iterable2))


def part2(lines: List[Tuple[Point, Point]], dimensions: Point) -> int:
    map = create_map(dimensions)
    for first, second in lines:
        abs_diff = combine(lambda a, b: abs(b - a), first, second)
        major_dimension: int = int(abs_diff[1] >= abs_diff[0])
        start, end = (second, first) if first[major_dimension] > second[major_dimension] else (
            first, second)
        direction = combine(lambda a, b: sign(b - a), start, end)
        current: List[int] = list(start)
        for i in range(0, abs_diff[major_dimension] + 1):
            map[current[1]][current[0]] += 1
            current = combine(lambda a, b: (a + b), current, direction)
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
