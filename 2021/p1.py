#!/usr/bin/env python3
from typing import List, Tuple

from aocd import numbers  # like [int(n) for n in data.splitlines()]
from aocd import submit
import functools

# quick solution
# def part1(numbers: List[int]) -> int:
#     count: int = 0
#     for index, number in enumerate(numbers[:-1]):
#         if number < numbers[index+1]:
#             count += 1
#     return count

# def part2(numbers: List[int]) -> int:
#     sums: List[int] = []
#     for index, number in enumerate(numbers[:-2]):
#         sums.append(number + numbers[index+1] + numbers[index+2])
#     return part1(sums)


# functional solution
def part1_reducer(context: Tuple[int, int], element: int) -> Tuple[int, int]:
    if context[0] < element:
        return (element, context[1] + 1)
    else:
        return (element, context[1])


def part1(numbers: List[int]) -> int:
    head, *tail = numbers
    return functools.reduce(part1_reducer, tail, (head, 0))[1]


def part2_reducer(context: Tuple[int, int, List[int]], element: int) -> Tuple[int, int, List[int]]:
    sum = element + context[0] + context[1]
    return (element, context[0], context[2] + [sum])


def part2(numbers: List[int]) -> int:
    return part1(functools.reduce(part2_reducer, numbers[2:], (numbers[1], numbers[0], []))[2])


def main():

    example: List[int] = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263,
    ]

    assert(part1(example) == 7)
    assert(part2(example) == 5)
    answer_a = part1(numbers)
    answer_b = part2(numbers)

    print(f"a {answer_a}")
    print(f"b {answer_b}")
    # a 1167
    # b 1130

    # if ready
    # submit(answer_a, part="a")
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
