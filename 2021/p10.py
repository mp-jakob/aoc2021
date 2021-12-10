#!/usr/bin/env python3
from typing import List, Dict
from aocd import lines, submit
import functools

bracket_error_score: Dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}

bracket_map: Dict[str, str] = {")": "(", "]": "[", "}": "{", ">": "<"}


def error_score(line: str) -> int:
    scopes: List[str] = []
    for char in line:
        if char not in bracket_map:
            scopes += [char]
        elif bracket_map[char] == scopes[-1]:
            scopes = scopes[:-1]
        else:
            return bracket_error_score[char]
    return 0


def part1(lines: List[str]) -> int:
    scores = list(map(error_score, lines))
    print(f"scores {scores}")
    return sum(scores)


def get_open_brackets(line: str) -> str:
    scopes: List[str] = []
    for char in line:
        if char not in bracket_map:
            scopes += [char]
        elif bracket_map[char] == scopes[-1]:
            scopes = scopes[:-1]
        else:
            return []
    return scopes


rev_bracket_map: Dict[str, str] = {"(": ")", "[": "]", "{": "}", "<": ">"}
bracket_close_score: Dict[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}


def part2(lines: List[str]) -> int:
    open_brackets: List[List[str]] = list(filter(lambda x: x, map(get_open_brackets, lines)))
    closes: List[str] = [[rev_bracket_map[char] for char in reversed(line)]for line in open_brackets]
    [print(close) for close in closes]
    scores = []
    for close in closes:
        score: int = 0
        for bracket in close:
            score = score * 5 + bracket_close_score[bracket]
            print(score)
        scores.append(score)
    print(scores)
    return sorted(scores)[len(scores) // 2]


def main():
    example: List[str] = [
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "{([(<{}[<>[]}>{[]{[(<()>",
        "(((({<>}<{<{<>}{[]{[]{}",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
        "<{([{{}}[<[[[<>{}]]]>[]]",
    ]

    assert(part1(example) == 26397)

    # displays = parse(lines)

    answer_a = part1(lines)
    print(f"a {answer_a}")
    assert(answer_a == 469755)
    # submit(answer_a, part="a")

    assert(part2(example) == 288957)

    answer_b = part2(lines)
    print(f"b {answer_b}")
    assert(answer_b == 2762335572)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
