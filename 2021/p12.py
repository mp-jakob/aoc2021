#!/usr/bin/env python3
from typing import List, Dict, Tuple
from aocd import lines, submit
from copy import deepcopy

Graph = Dict[str, List[str]]


def parse(lines: List[str]) -> Graph:
    graph: Graph = {}
    for line in lines:
        a, b = line.strip().split('-')
        if a not in graph:
            graph.update({a: [b]})
        else:
            graph[a] += [b]
        if b not in graph:
            graph.update({b: [a]})
        else:
            graph[b] += [a]
    return graph


def recurse(graph: Graph, path) -> List[str]:
    if path[-1] == 'end':
        return [path]
    else:
        paths: List[str] = []
        for neighbour in graph[path[-1]]:
            if neighbour[0].isupper() or neighbour not in path:
                paths += recurse(graph, path + [neighbour])
    return paths


def part1(graph: Graph) -> int:
    paths = recurse(graph, ['start'])
    return len(paths)


def part2(graph: Graph) -> int:
    paths: List[List[str]] = []
    worklist: List[Tuple[List[str], str]] = [(["start"], False)]
    while len(worklist):
        context, *worklist = worklist
        path, double = context
        if path[-1] == 'end':
            paths += [path]
        else:
            for neighbour in graph[path[-1]]:
                if neighbour[0].isupper():
                    worklist += [(path + [neighbour], double)]
                elif neighbour != "start":
                    if neighbour not in path:
                        worklist += [(path + [neighbour], double)]
                    elif not double:
                        worklist += [(path + [neighbour], True)]

    # [print(path) for path in paths]
    return len(paths)


def main():
    example: List[str] = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ]

    example2: List[str] = [
        "dc-end",
        "HN-start",
        "start-kj",
        "dc-start",
        "dc-HN",
        "LN-dc",
        "HN-end",
        "kj-sa",
        "kj-HN",
        "kj-dc",
    ]
    example3: List[str] = [
        "fs-end",
        "he-DX",
        "fs-he",
        "start-DX",
        "pj-DX",
        "end-zg",
        "zg-sl",
        "zg-pj",
        "pj-he",
        "RW-he",
        "fs-DX",
        "pj-RW",
        "zg-RW",
        "start-pj",
        "he-WI",
        "zg-he",
        "pj-fs",
        "start-RW",
    ]

    example_cave = parse(example)

    assert(part1(example_cave) == 10)
    assert(part1(parse(example2)) == 19)
    assert(part1(parse(example3)) == 226)

    cave = parse(lines)
    answer_a = part1(cave)
    print(f"a {answer_a}")
    assert(answer_a == 3485)
    # submit(answer_a, part="a")

    assert(part2(example_cave) == 36)
    assert(part2(parse(example2)) == 103)
    assert(part2(parse(example3)) == 3509)

    answer_b = part2(cave)
    print(f"b {answer_b}")
    assert(answer_b == 85062)
    # submit(answer_b, part="b")


if __name__ == "__main__":
    main()
