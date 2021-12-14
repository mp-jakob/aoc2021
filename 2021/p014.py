#!/usr/bin/env python3
from typing import List, Tuple, Dict
from aocd import lines, submit
from copy import deepcopy
from functools import reduce

Insertions = Dict[str, str]
Histogram = Dict[str, int]


def parse(lines: List[str]) -> Tuple[str, Insertions]:
    insertions = dict(map(lambda line: (line[:2], line[6]), lines[2:]))
    return (lines[0].strip(), insertions)


def expand(histogram: Histogram, insertions: Insertions, frequencies: Histogram) -> Tuple[Histogram, Histogram]:
    expanded = deepcopy(histogram)
    for pair, occurences in histogram.items():
        inserter = insertions[pair]
        if pair[0] + inserter not in expanded:
            expanded[pair[0] + inserter] = 0
        expanded[pair[0] + inserter] += occurences
        if inserter + pair[1] not in expanded:
            expanded[inserter + pair[1]] = 0
        expanded[inserter + pair[1]] += occurences
        expanded[pair] -= occurences
        if not inserter in frequencies:
            frequencies[inserter] = 0
        frequencies[inserter] += occurences
    return (expanded, frequencies)


def solution(template: str, insertions: Insertions, iterations: int) -> int:

    def letter_counter(table, char):
        if char not in table:
            table[char] = 0
        table[char] += 1
        return table

    frequencies = reduce(letter_counter, template, {})

    histogram: Histogram = {}
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        if not pair in histogram:
            histogram[pair] = 1
        else:
            histogram[pair] += 1

    for i in range(iterations):
        histogram, frequencies = expand(histogram, insertions, frequencies)

    most_common = max(frequencies.values())
    least_common = min(frequencies.values())
    return most_common - least_common


def main():
    example: List[str] = [
        "NNCB",
        "",
        "CH -> B",
        "HH -> N",
        "CB -> H",
        "NH -> C",
        "HB -> C",
        "HC -> B",
        "HN -> C",
        "NN -> C",
        "BH -> H",
        "NC -> B",
        "NB -> B",
        "BN -> B",
        "BB -> N",
        "BC -> B",
        "CC -> N",
        "CN -> C",
    ]

    example_template, example_insertions = parse(example)
    assert(solution(example_template, example_insertions, 10) == 1588)

    template, inserrions = parse(lines)
    answer_a = solution(template, inserrions, 10)
    print(f"a {answer_a}")
    assert(answer_a == 2797)
    # submit(answer_a, part="a")

    assert(solution(example_template, example_insertions, 40) == 2188189693529)
    answer_b = solution(template, inserrions, 40)
    print(f"b {answer_b}")

    assert(answer_b == 2926813379532)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
