#!/usr/bin/env python3
from typing import List, Tuple
from aocd import lines
from aocd import submit
import functools


def parse(lines: List[str]) -> List[List[int]]:
    matrix: List[List[int]] = []
    for line in lines:
        matrix.append([int(char) for char in line])
    return matrix


def bitlist_to_int(binary: List[int]) -> int:
    def constructor(accumulator, bit): return (accumulator << 1) + bit
    return functools.reduce(constructor, binary, 0)


def calculate_histogramm(matrix: List[List[int]]) -> List[int]:
    def summator(row, accumulator): return [
        sum(list(pair)) for pair in zip(row, accumulator)]
    # https: // stackoverflow.com/a/8528626q
    histogramm = functools.reduce(summator, matrix, [0] * len(matrix[0]))
    # print(f"{histogramm}")
    return histogramm


def ones_complement(val: int, digits: int) -> int:
    return val ^ ((1 << digits) - 1)


def calculate_gamma(histogramm: List[int], num_entries: int) -> List[int]:
    gamma = [(count >= (num_entries + 1) // 2) for count in histogramm]
    # print(
    #     f"gamma of {histogramm} with {num_entries} entries is {bin(gamma)}")
    return gamma


def part1(matrix: List[List[int]]) -> int:
    digits: int = len(matrix[0])

    histogramm = calculate_histogramm(matrix)
    gamma = bitlist_to_int(calculate_gamma(histogramm, len(matrix)))
    return gamma * ones_complement(gamma, digits)


def calculate_oxygen(matrix: List[List[int]]) -> int:
    digits: int = len(matrix[0])
    matches = matrix
    for i in range(digits):
        histogramm = calculate_histogramm(matches)
        digit = (calculate_gamma(histogramm, len(matches)))[i]
        matches = [number for number in matches if
                   (number[i]) % 2 == digit]
        # print(f"for {digit} got {len(matches)}: ", end="")
        # [print(bin(bitlist_to_int(match)), end=", ") for match in matches]
        # print("")
        if len(matches) == 1:
            return bitlist_to_int(matches[0])
    return None


def calculate_co2(matrix: List[List[int]]) -> int:
    digits: int = len(matrix[0])
    matches = matrix
    for i in range(digits):
        histogramm = calculate_histogramm(matches)
        digit = 1 - calculate_gamma(histogramm, len(matches))[i]
        matches = [number for number in matches if
                   (number[i]) % 2 == digit]
        # print(f"for {digit} got {len(matches)}: ", end="")
        # [print(bin(bitlist_to_int(match)), end=", ") for match in matches]
        # print("")
        if len(matches) == 1:
            return bitlist_to_int(matches[0])
    return None


def part2(matrix: List[List[int]]) -> int:
    oxygen = calculate_oxygen(matrix)
    # print("oxygen: " + bin(oxygen))
    co2 = calculate_co2(matrix)
    # print("co2: " + bin(co2))
    return oxygen * co2

# functional solution


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
    assert(calculate_oxygen(example_numbers) == 23)
    assert(calculate_co2(example_numbers) == 10)
    answer_b = part2(numbers)

    print(f"b {answer_b}")
    assert(answer_b == 4105235)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
