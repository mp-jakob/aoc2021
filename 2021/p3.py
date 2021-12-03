#!/usr/bin/env python3
from typing import List
from aocd import lines
from aocd import submit
import functools


def parse(lines: List[str]) -> List[List[int]]:
    return [
        [int(char) for char in line]
        for line in lines]


def bitlist_to_int(binary: List[int]) -> int:
    def constructor(accumulator, bit): return (accumulator << 1) + bit
    return functools.reduce(constructor, binary, 0)


def majority_bit(matrix: List[List[int]], column: int) -> int:
    def summator(accumulator, row): return row[column] + accumulator
    column_sum = functools.reduce(summator, matrix, 0)
    # calculate if sum is at last half of total count
    return column_sum >= (len(matrix) + 1) // 2


def part1(matrix: List[List[int]]) -> int:
    gamma = bitlist_to_int(
        [majority_bit(matrix, i) for i in range(len(matrix[0]))]
    )
    # calculate one's complement
    epsilon = gamma ^ ((1 << len(matrix[0])) - 1)
    return gamma * epsilon


def majority_matcher(matrix: List[List[int]], column: int, invert: bool) -> int:
    if len(matrix) == 1:
        return bitlist_to_int(matrix[0])
    else:
        bit = majority_bit(matrix, column)
        matches = [number for number in matrix if
                   number[column] == (1 - bit if invert else bit)]
        return majority_matcher(matches, column + 1, invert)


def part2(matrix: List[List[int]]) -> int:
    oxygen = majority_matcher(matrix, 0, invert=False)
    co2 = majority_matcher(matrix, 0, invert=True)
    return oxygen * co2


def main():
    example: List[str] = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]

    example_numbers = parse(example)
    assert(part1(example_numbers) == 198)

    numbers = parse(lines)
    answer_a = part1(numbers)

    print(f"a {answer_a}")
    assert(answer_a == 3847100)
    # submit(answer_a, part="a")

    assert(part2(example_numbers) == 230)
    answer_b = part2(numbers)

    print(f"b {answer_b}")
    assert(answer_b == 4105235)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
