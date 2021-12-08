#!/usr/bin/env python3
from typing import List, Dict
from aocd import lines, submit
import functools
from collections import namedtuple

Display = namedtuple('Display', ['patterns', 'outputs'])


def parse(lines: List[str]) -> List[Display]:
    displays: List[Display] = []
    for line in lines:
        patterns, outputs = line.split("|")
        displays.append(Display(patterns.strip().split(" "),
                        outputs.strip().split(" ")))
    return displays


def part1(displays: List[Display]) -> int:
    count: int = 0
    for _, outputs in displays:
        for output in outputs:
            length: int = len(output)
            if length == 2 or length == 3 or length == 4 or length == 7:
                count += 1
    return count


def contained_in(a: str, b: str) -> bool:
    temp = set(list(a))
    for char in b:
        temp.discard(char)
    return not temp


def list_to_str(list: List[str]) -> str:
    return "".join(list)


def map_output(display: Display) -> Dict[str, int]:
    mapping: Dict(str, int) = dict()
    one = list_to_str(
        sorted(next(filter(lambda x: len(x) == 2, display.patterns))))
    four = list_to_str(
        sorted(next(filter(lambda x: len(x) == 4, display.patterns))))
    seven = list_to_str(
        sorted(next(filter(lambda x: len(x) == 3, display.patterns))))
    eight = list_to_str(
        sorted(next(filter(lambda x: len(x) == 7, display.patterns))))
    mapping[one] = 1
    mapping[four] = 4
    mapping[seven] = 7
    mapping[eight] = 8
    three = list_to_str(sorted(next(filter(lambda x: len(x) ==
                                           5 and contained_in(one, x), display.patterns))))
    nine = list_to_str(sorted(next(filter(lambda x: len(x) ==
                                          6 and contained_in(three, x), display.patterns))))
    zero = list_to_str(sorted(next(filter(lambda x: len(x) ==
                                          6 and contained_in(one, x) and list_to_str(sorted(x)) != nine, display.patterns))))
    six = list_to_str(sorted(next(filter(lambda x: len(x) ==
                                         6 and list_to_str(sorted(x)) != nine and list_to_str(sorted(x)) != zero, display.patterns))))
    five = list_to_str(sorted(next(filter(lambda x: len(x) ==
                                          5 and contained_in(x, nine) and list_to_str(sorted(x)) != three, display.patterns))))
    two = list_to_str(sorted(next(filter(lambda x: len(x) ==
                                         5 and list_to_str(sorted(x)) != five and list_to_str(sorted(x)) != three, display.patterns))))
    assert(zero not in mapping)
    mapping.update({zero: 0})
    assert(two not in mapping)
    mapping.update({two: 2})
    assert(three not in mapping)
    mapping.update({three: 3})
    assert(five not in mapping)
    mapping.update({five: 5})
    assert(six not in mapping)
    mapping.update({six: 6})
    assert(nine not in mapping)
    mapping.update({nine: 9})

    return mapping


def decode(display: Display) -> int:
    signal_map = map_output(display)
    # print(signal_map)
    number: int = 0
    for output in display.outputs:
        number = number * 10 + signal_map[list_to_str(sorted(output))]
    # print(number)
    return number


def part2(displays: List[Display]) -> int:
    return sum(map(decode, displays))


def main():
    example: List[str] = [
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
    ]

    example_displays = parse(example)
    print(example_displays)
    assert(part1(example_displays) == 26)

    displays = parse(lines)

    answer_a = part1(displays)
    print(f"a {answer_a}")
    assert(answer_a == 543)
    # submit(answer_a, part="a")

    example_line = [
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]
    data = parse(example_line)
    assert(decode(data[0]) == 5353)
    assert(part2(example_displays) == 61229)

    answer_b = part2(displays)
    print(f"b {answer_b}")
    assert(answer_b == 994266)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
