import time
import re
from collections import defaultdict


def read_input(path):
    result = []

    with open(path, "r") as file:
        result = [
            [[int(y) for y in x.split(",")] for x in re.findall("[0-9]+,[0-9]+", line)]
            for line in file.readlines()
        ]

    return result


def cover_points(p1, p2, points):
    dist_x, dist_y = p2[0] - p1[0], p2[1] - p1[1]
    step_x = dist_x // abs(dist_x) if dist_x != 0 else 0
    step_y = dist_y // abs(dist_y) if dist_y != 0 else 0

    points[tuple(p1)] += 1

    x_curr, y_curr = p1
    while y_curr != p2[1] or x_curr != p2[0]:
        x_curr += step_x
        y_curr += step_y
        points[(x_curr, y_curr)] += 1


def solve_silver(puzzle):
    points = defaultdict(lambda: 0)

    for p1, p2 in puzzle:
        if p1[0] == p2[0] or p1[1] == p2[1]:
            cover_points(p1, p2, points)

    count = len([x for x in points if points[x] > 1])

    return count


def solve_gold(puzzle):
    points = defaultdict(lambda: 0)

    for p1, p2 in puzzle:
        cover_points(p1, p2, points)

    count = len([x for x in points if points[x] > 1])

    return count


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
