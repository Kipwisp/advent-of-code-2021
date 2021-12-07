import time
import numpy as np


def read_input(path):
    result = []

    with open(path, "r") as file:
        return [int(x) for x in file.readline().split(",")]


def simulate(puzzle, days):
    stages = 9
    population = [0] * stages
    for x in puzzle:
        population[x] += 1

    matrix = np.array(
        [
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )

    population = np.matmul(np.linalg.matrix_power(matrix, days), population)

    return sum(population)


def solve_silver(puzzle):
    days = 80
    return simulate(puzzle, days)


def solve_gold(puzzle):
    days = 256
    return simulate(puzzle, days)


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
