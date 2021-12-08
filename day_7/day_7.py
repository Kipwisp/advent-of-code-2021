import time
import math


def read_input(path):
    result = []

    with open(path, "r") as file:
        return [int(x) for x in file.readline().split(",")]


def solve_silver(puzzle):
    pos = sorted(puzzle)[len(puzzle) // 2]

    cost = 0
    for x in puzzle:
        cost += abs(x - pos)

    return cost


def solve_gold(puzzle):
    pos = sum(puzzle) // len(puzzle)

    cost = 0
    for crab in puzzle:
        cost += (abs(crab - pos) * (abs(crab - pos) + 1)) // 2

    return cost


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(puzzle)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
