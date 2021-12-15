import time
from collections import defaultdict
import math


def read_input(path):
    with open(path, "r") as file:
        template, mappings = file.read().split("\n\n")

        rules = {}
        for line in mappings.split("\n"):
            pair, polymer = line.split(" -> ")

            rules[pair] = (pair[0] + polymer, polymer + pair[1])

        return template, rules


def process(steps, template, rules):
    counts = defaultdict(int)
    pairs = defaultdict(int)

    for i in range(len(template)):
        if i != len(template) - 1:
            pair = template[i] + template[i + 1]
            pairs[pair] += 1

        counts[template[i]] += 1

    for _ in range(steps):
        new_pairs = defaultdict(int)
        for pair in pairs:
            for child in rules[pair]:
                new_pairs[child] += pairs[pair]

            counts[child[0]] += pairs[pair]

        pairs = new_pairs

    return max(v for v in counts.values()) - min(v for v in counts.values())


def solve_silver(template, rules):
    return process(10, template, rules)


def solve_gold(template, rules):
    return process(40, template, rules)


def main():
    path = "input.txt"
    template, rules = read_input(path)

    start = time.time()
    silver = solve_silver(template, rules)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(template, rules)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
