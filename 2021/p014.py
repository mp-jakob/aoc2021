#!/usr/bin/env python3
from typing import List, Tuple, Dict
from aocd import lines, submit
from copy import deepcopy
from functools import reduce

Insertions = Dict[str, str]


def parse(lines: List[str]) -> Tuple[str, Insertions]:
    insertions = dict(map(lambda line: (line[:2], line[6]), lines[2:]))
    return (lines[0].strip(), insertions)


def expand(template: str, insertions: Insertions) -> str:
    expanded = ""
    for i in range(len(template) - 1):
        head, next, *tail = template
        expanded += template[i] + insertions[template[i:i+2]]
    expanded += template[len(template) - 1]
    return expanded


def part1(template: str, insertions: Insertions, iterations: int) -> int:
    for i in range(iterations):
        print(i)
        template = expand(template, insertions)

    def letter_counter(table, curr):
        if curr not in table:
            table[curr] = 1
        else:
            table[curr] += 1
        return table

    frequencies = reduce(letter_counter, template, {})
    print(frequencies)
    most_common = max(frequencies.values())
    least_common = min(frequencies.values())
    print(f"{least_common} and  {most_common}")
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
    print(example_template)
    print(example_insertions)
    assert(part1(example_template, example_insertions, 10) == 1588)

    template, inserrions = parse(lines)
    answer_a = part1(template, inserrions, 10)
    print(f"a {answer_a}")
    assert(answer_a == 2797)
    # submit(answer_a, part="a")

    assert(part1(example_template, example_insertions, 40) == 2188189693529)
    # # part2(example_template, example_insertions)
    # print(f"b")
    answer_b = part1(template, inserrions, 40)
    print(f"b {answer_b}")
    # [print(row) for row in answer_b]

    # assert(answer_b == solution)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
