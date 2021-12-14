#!/usr/bin/env python3
from typing import List, Tuple, Dict
from aocd import lines, submit
from copy import deepcopy
from functools import reduce
from collections import defaultdict

Insertions = Dict[str, str]
Histogram = Dict[str, int]


def parse(lines: List[str]) -> Tuple[str, Insertions]:
    insertions = dict(map(lambda line: (line[:2], line[6]), lines[2:]))
    return (lines[0].strip(), insertions)


def expand(histogram: Histogram, insertions: Insertions, frequencies: Histogram) -> Tuple[Histogram, Histogram]:
    def histogram_reducer(frequencies, item):
        pair, occurences = item
        inserter = insertions[pair]
        frequencies[pair[0] + inserter] += occurences
        frequencies[inserter + pair[1]] += occurences
        frequencies[pair] -= occurences
        return frequencies

    expanded = reduce(histogram_reducer, histogram.items(),
                      deepcopy(histogram))

    def frequency_reducer(frequencies, item):
        pair, occurences = item
        inserter = insertions[pair]
        frequencies[inserter] += occurences
        return frequencies

    frequencies = reduce(frequency_reducer, histogram.items(), frequencies)
    return (expanded, frequencies)


def solution(template: str, insertions: Insertions, iterations: int) -> int:

    def letter_counter(table, char):
        table[char] += 1
        return table

    # https: // docs.python.org/3.8/library/collections.html
    frequencies: Histogram = reduce(
        letter_counter, template, defaultdict(lambda: 0))

    def pair_counter(histogram, i):
        pair = template[i:i+2]
        histogram[pair] += 1
        return histogram

    histogram: Histogram = reduce(pair_counter, range(
        len(template) - 1), defaultdict(lambda: 0))

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
