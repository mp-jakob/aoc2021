#!/usr/bin/env python3
from typing import List, Tuple
from aocd import lines, submit
from operator import and_, countOf
from functools import reduce

# from copy import deepcopy

Map = List[List[int]]
Fold = Tuple[str, int]


def elementwise(func, iterable1, iterable2):
    return list(map(func, iterable1, iterable2))


def create_map(dimensions: Tuple[int, int]) -> Map:
    # prevent shallow copy of rows
    # https://stackoverflow.com/a/13347704
    return [
        [0 for i in range(dimensions[1])]
        for i in range(dimensions[0])]


def parse(lines: List[str]) -> Tuple[Map, List[Fold]]:
    dimensions: Tuple[int, int] = (0, 0)
    points: List[Tuple[int, int]] = []

    line_iterator = iter(lines)
    for line in line_iterator:
        line = line.strip()
        if not line:
            break
        x, y = list(map(int, line.split(',')))
        points.append((y, x))
        dimensions = elementwise(max, dimensions, (y + 1, x + 1))

    folds: List[Fold] = []
    for line in line_iterator:
        folds.append((line[11], int(line[13:])))

    paper = create_map(dimensions)
    for point in points:
        paper[point[0]][point[1]] = 1
    return (paper, folds)


def fold(paper: Map, fold: Fold) -> Map:
    # fold up
    if fold[0] == 'y':
        top, bottom = paper[:fold[1]], paper[fold[1] + 1:]
        if len(top) > len(bottom):
            bottom += create_map((len(top) - len(bottom), len(top[0])))
        elif len(top) < len(bottom):
            top = create_map((len(top) - len(bottom), len(top[0]))) + top
        assert(len(top) == len(bottom))
        paper = list(
            map(lambda x, y: elementwise(lambda x, y: x or y, x, y), top, reversed(bottom)))
    else:
        new = []
        for row in paper:
            left, right = row[:fold[1]], row[fold[1] + 1:]
            assert(len(left) == len(right))
            new_row = list(
                map(lambda x, y: x or y, left, reversed(right)))
            new.append(new_row)
        paper = new
    return paper


def part1(paper: Map, folds: List[Fold]) -> int:
    paper = fold(paper, folds[0])
    num_dots = reduce(lambda total, row: total + sum(row), paper, 0)
    return num_dots


def part2(paper: Map, folds: List[Fold]) -> int:
    for folding in folds:
        paper = fold(paper, folding)
    [print(row) for row in paper]
    return 0


def main():
    example: List[str] = [
        "6,10",
        "0,14",
        "9,10",
        "0,3",
        "10,4",
        "4,11",
        "6,0",
        "6,12",
        "4,1",
        "0,13",
        "10,12",
        "3,4",
        "3,0",
        "8,4",
        "1,10",
        "2,14",
        "8,10",
        "9,0",
        "",
        "fold along y=7",
        "fold along x=5",
    ]

    example_paper, example_folds = parse(example)

    assert(part1(example_paper, example_folds) == 17)

    paper, folds = parse(lines)
    answer_a = part1(paper, folds)
    print(f"a {answer_a}")
    assert(answer_a == 735)
    # submit(answer_a, part="a")

    # part2(example_paper, example_folds)
    print(f"b")
    answer_b = part2(paper, folds)
    # assert(answer_b == 85062)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
