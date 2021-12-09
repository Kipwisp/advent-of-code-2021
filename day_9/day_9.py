import time
import math


def read_input(path):
    with open(path, "r") as file:
        puzzle = [[int(x) for x in line.strip()] for line in file.readlines()]

        row_length = len(puzzle[0])
        puzzle.insert(0, [math.inf] * row_length)
        puzzle.append([math.inf] * row_length)
        for row in puzzle:
            row.insert(0, math.inf)
            row.append(math.inf)

        return puzzle


def solve_silver(puzzle):
    low_points = []
    risk_levels = []

    for r in range(1, len(puzzle) - 1):
        for c in range(1, len(puzzle[0]) - 1):
            adjacent = [
                puzzle[r + 1][c],
                puzzle[r - 1][c],
                puzzle[r][c + 1],
                puzzle[r][c - 1],
            ]

            if puzzle[r][c] < min(adjacent):
                low_points.append([r, c])
                risk_levels.append(puzzle[r][c] + 1)

    return sum(risk_levels), low_points


def expand_basin(point, puzzle, visited):
    size = 1
    r, c = point
    adjacent = [
        [r + 1, c],
        [r - 1, c],
        [r, c + 1],
        [r, c - 1],
    ]

    visited.add((r, c))
    for ra, ca in adjacent:
        adj = puzzle[ra][ca]
        if adj not in {9, math.inf} and (ra, ca) not in visited:
            size += expand_basin([ra, ca], puzzle, visited)

    return size


def solve_gold(puzzle, low_points):
    basins = [0] * 3
    for r, c in low_points:
        visited = set()
        size = expand_basin([r, c], puzzle, visited)

        if size > min(basins):
            basins.pop(0)
            basins.append(size)

    return math.prod(basins)


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver, low_points = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(puzzle, low_points)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
