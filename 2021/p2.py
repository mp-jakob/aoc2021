#!/usr/bin/env python3
from typing import List, Tuple
from enum import Enum
from aocd import lines
from aocd import submit
import functools
from collections import namedtuple

Command = namedtuple('Command', ['direction', 'amount'])
State1 = namedtuple('State1', ['horizontal', 'depth'], defaults=[0, 0])
State2 = namedtuple(
    'State2', ['horizontal', 'depth', 'aim'], defaults=[0, 0, 0])


class Direction(Enum):
    FORWARD = 0,
    UP = 1,
    DOWN = 2

    # https: // stackoverflow.com/a/49060635
    @staticmethod
    def from_str(label):
        if label == "forward":
            return Direction.FORWARD
        elif label == "up":
            return Direction.UP
        elif label == "down":
            return Direction.DOWN
        else:
            raise NotImplementedError


def parse(lines: List[str]) -> List[Command]:
    split = [line.split() for line in lines]
    parsed: List[Command] = []
    for direction_str, amount in split:
        parsed.append(Command(Direction.from_str(direction_str), int(amount)))
    return parsed


# quick solution
# def part1(commands: List[Command]) -> int:
#     horizontal: int = 0
#     depth: int = 0
#     for direction, amount in commands:
#         if (direction == Direction.FORWARD):
#             horizontal += amount
#         elif direction == Direction.UP:
#             depth -= amount
#         elif direction == Direction.DOWN:
#             depth += amount
#     return horizontal * depth


# def part2(commands: List[Command]) -> int:
#     horizontal: int = 0
#     depth: int = 0
#     aim: int = 0
#     for direction, amount in commands:
#         if (direction == Direction.FORWARD):
#             horizontal += amount
#             depth += aim * amount
#         elif direction == Direction.UP:
#             aim -= amount
#         elif direction == Direction.DOWN:
#             aim += amount
#     return horizontal * depth


# functional solution
def part1_reducer(context: State1, command: Command) -> State1:
    if (command.direction == Direction.FORWARD):
        return State1(context.horizontal + command.amount, context.depth)
    elif command.direction == Direction.UP:
        return State1(context.horizontal, context.depth - command.amount)
    else:
        return State1(context.horizontal, context.depth + command.amount)


def part1(commands: List[Command]) -> int:
    horizontal, depth = functools.reduce(part1_reducer, commands, State1())
    return horizontal * depth


def part2_reducer(context: State2, command: Command) -> State2:
    if (command.direction == Direction.FORWARD):
        return State2(context.horizontal + command.amount, context.depth + context.aim * command.amount, context.aim)
    elif command.direction == Direction.UP:
        return State2(context.horizontal, context.depth, context.aim - command.amount)
    else:
        return State2(context.horizontal, context.depth, context.aim + command.amount)


def part2(commands: List[Command]) -> int:
    horizontal, depth, _ = functools.reduce(
        part2_reducer, commands, State2())
    return horizontal * depth


def main():
    example: List[str] = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]

    example_commands = parse(example)
    assert(part1(example_commands) == 150)
    assert(part2(example_commands) == 900)

    commands = parse(lines)
    answer_a = part1(commands)
    answer_b = part2(commands)

    print(f"a {answer_a}")
    print(f"b {answer_b}")
    # a 1507611
    # b 1880593125

    # if ready
    assert(answer_a == 1507611)
    assert(answer_b == 1880593125)
    # submit(answer_a, part="a")
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
