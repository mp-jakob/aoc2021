#!/usr/bin/env python3
from typing import List, Tuple, TypeVar
from aocd import lines, submit
from operator import add
from functools import reduce

Map = List[List[int]]
Fold = Tuple[str, int]
T = TypeVar('T')


def combine_lists(func, iterable1, iterable2):
    return list(map(func, iterable1, iterable2))


def create_map(dimensions: Tuple[int, int]) -> Map:
    # prevent shallow copy of rows
    # https://stackoverflow.com/a/13347704
    return [
        [0 for i in range(dimensions[1])]
        for i in range(dimensions[0])]


def parse(lines: List[str]) -> Tuple[Map, List[Fold]]:
    point_lines = lines[:lines.index("")]
    points = [tuple(map(int, reversed(line.split(','))))
              for line in point_lines]

    dimensions = reduce(lambda acc, x: map(
        max, acc, x), points, (0, 0))
    dimensions = tuple(map(add, dimensions, (1, 1)))

    fold_lines = lines[lines.index("") + 1:]
    folds = [((line[11], int(line[13:])))
             for line in fold_lines]

    paper = create_map(dimensions)
    for point in points:
        paper[point[0]][point[1]] = 1
    return (paper, folds)


def split_at(list: List[T], index: int) -> Tuple[List[T], List[T]]:
    return list[:index], list[index + 1:]


def fold(paper: Map, fold: Fold) -> Map:
    # fold up
    if fold[0] == 'y':
        top, bottom = split_at(paper, fold[1])
        # pad halves in case the fold is not centered
        bottom += create_map((max(0, len(top) - len(bottom)), len(top[0])))
        top = create_map(
            (max(0, len(top) - len(bottom)), len(top[0]))) + top
        return [combine_lists(lambda x, y: x or y, x, y)
                for x, y in zip(top, reversed(bottom))]
    # fold left
    else:
        # no let expression in python, so we need to define a local function
        def folder(row):
            left, right = split_at(row, fold[1])
            return [x or y for x, y in zip(left, reversed(right))]
        return [folder(row) for row in paper]


def part1(paper: Map, folds: List[Fold]) -> int:
    paper = fold(paper, folds[0])
    num_dots = sum(map(lambda row: sum(row), paper))
    return num_dots


def part2(paper: Map, folds: List[Fold]) -> Map:
    if folds:
        head, *tail = folds
        return part2(fold(paper, head), tail)
    else:
        return paper


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
    [print(row) for row in answer_b]

    solution: Map = [
        [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1,
            0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1,
            0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1,
            0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    ]
    assert(answer_b == solution)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
