#!/usr/bin/env python3
from typing import List, Tuple, Dict
from aocd import lines
from aocd import submit
import functools
import re

Board = List[List[int]]
Occurences = Dict[int, List[Tuple[int, int, int]]]


def parse(lines: List[str]) -> Tuple[List[int], List[Board], Occurences]:
    drawn: List[int] = [int(number) for number in lines[0].split(",")]
    boards: List[Board] = []
    occurences: Occurences = dict()
    for line in lines[1:]:
        if not line:
            boards.append([])
        else:
            # https://stackoverflow.com/a/8113811
            row_numbers: List[int] = [int(x)
                                      for x in re.split('\s+', line.strip())]
            boards[-1].append(row_numbers)
            for i, number in enumerate(row_numbers):
                if number not in occurences:
                    occurences[number] = []
                occurences[number].append(
                    (len(boards) - 1, len(boards[-1]) - 1, i))
    return (drawn, boards, occurences)


def empty_boards(boards: int, rows: int, columns: int) -> List[Board]:
    # prevent shallow copy of rows
    # https://stackoverflow.com/a/13347704
    return [[[0 for i in range(columns)] for i in range(rows)]for i in range(boards)]


def column_full(board: Board, column: int) -> int:
    def summator(accumulator, row): return row[column] + accumulator
    return functools.reduce(summator, board, 0) == len(board)


def row_full(board: Board, row: int) -> int:
    return sum(board[row]) == len(board[row])


def unmarked_row_sum(row: List[int], mark_row: List[int]):
    return sum([number * (1 - mark) for number, mark in zip(row, mark_row)])


def unmarked_board_sum(board: Board, marks: Board) -> int:
    return sum([unmarked_row_sum(row, mark_row) for row, mark_row in zip(board, marks)])


def part1(boards: List[Board], drawn: List[int], occurences: Occurences) -> int:
    marks: List[Board] = empty_boards(
        len(boards), len(boards[0][0]), len(boards[0]))
    for number in drawn:
        for board, row, column in occurences[number]:
            marks[board][row][column] = 1
            if column_full(marks[board], column) or row_full(marks[board], row):
                return unmarked_board_sum(boards[board], marks[board]) * number

    return -1


def part2(boards: List[Board], drawn: List[int], occurences: Occurences) -> int:
    marks: List[Board] = empty_boards(
        len(boards), len(boards[0][0]), len(boards[0]))
    not_won: List[int] = [i for i in range(len(boards))]
    for number in drawn:
        for board, row, column in occurences[number]:
            marks[board][row][column] = 1
            if column_full(marks[board], column) or row_full(marks[board], row):
                if board in not_won:
                    not_won.remove(board)
                    if not not_won:
                        return unmarked_board_sum(boards[board], marks[board]) * number
    return -1


def main():
    example: List[str] = [
        "7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1",
        "",
        "22 13 17 11  0",
        "8  2 23  4 24",
        "21  9 14 16  7",
        "6 10  3 18  5",
        "1 12 20 15 19",
        "",
        "3 15  0  2 22",
        "9 18 13 17  5",
        "19  8  7 25 23",
        "20 11 10 24  4",
        "14 21 16 12  6",
        "",
        "14 21 17 24  4",
        "10 16 15  9 19",
        "18  8 23 26 20",
        "22 11 13  6  5",
        "2  0 12  3  7",
    ]

    example_numbers, example_boards, example_occurences = parse(example)
    assert(part1(example_boards, example_numbers, example_occurences) == 4512)

    # numbers = parse(lines)
    numbers, boards, occurences = parse(lines)
    answer_a = part1(boards, numbers, occurences)

    print(f"a {answer_a}")
    assert(answer_a == 82440)
    # submit(answer_a, part="a")

    assert(part2(example_boards, example_numbers, example_occurences) == 1924)
    answer_b = part2(boards, numbers, occurences)

    print(f"b {answer_b}")
    assert(answer_b == 20774)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
