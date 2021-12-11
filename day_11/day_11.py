import time
import math
import copy


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


def flash(point, puzzle, flashed):
    flashes = 1
    r, c = point
    adjacent = [
        [r + i, c + j] for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]

    flashed.add((r, c))
    puzzle[r][c] = 0

    for ra, ca in adjacent:
        if (ra, ca) not in flashed:
            puzzle[ra][ca] += 1
            adj = puzzle[ra][ca]
            if adj == 10:
                flashes += flash([ra, ca], puzzle, flashed)

    return flashes


def charge(puzzle):
    flashes = 0
    flashing = []
    for r in range(1, len(puzzle) - 1):
        for c in range(1, len(puzzle[0]) - 1):
            puzzle[r][c] += 1
            if puzzle[r][c] == 10:
                flashing.append((r, c))

    flashed = set()
    for r, c in flashing:
        if (r, c) not in flashed:
            flashes += flash([r, c], puzzle, flashed)

    return flashes, flashed


def solve_silver(puzzle):
    flashes = 0
    steps = 100

    for _ in range(steps):
        new_flashes, _ = charge(puzzle)

        flashes += new_flashes

    return flashes


def solve_gold(puzzle):
    octo_count = 100

    step = 0
    flashed = set()
    while len(flashed) != octo_count:
        _, flashed = charge(puzzle)
        step += 1

    return step


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver = solve_silver(copy.deepcopy(puzzle))
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(copy.deepcopy(puzzle))
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
