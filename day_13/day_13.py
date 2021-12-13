import time
import re
import copy


def read_input(path):
    dots = set()
    folds = []
    with open(path, "r") as file:
        points, instructions = "".join(file.readlines()).split("\n\n")

        for line in points.split("\n"):
            x, y = line.strip().split(",")
            dots.add((int(x), int(y)))

        for line in instructions.split("\n"):
            axis, pos = re.search("[xy]=[0-9]+", line.strip()).group().split("=")
            folds.append((axis, int(pos)))

    return dots, folds


def fold(axis, pos, points):
    result = set()

    for x, y in points:
        if axis == "x" and x > pos:
            result.add((-x + 2 * pos, y))
        elif axis == "y" and y > pos:
            result.add((x, -y + 2 * pos))
        else:
            result.add((x, y))

    return result


def print_dots(dots):
    width = max([x for x, _ in dots]) + 1
    height = max([y for _, y in dots]) + 1

    map = [
        ["▮" if (j, i) in dots else " " for j in range(width)] for i in range(height)
    ]

    for row in map:
        print("".join(row))


def solve_silver(dots, folds):
    result = dots
    for axis, pos in folds:
        result = fold(axis, pos, result)
        break

    return len(result)


def solve_gold(dots, folds):
    result = dots
    for axis, pos in folds:
        result = fold(axis, pos, result)

    return result


def main():
    path = "input.txt"
    dots, folds = read_input(path)

    start = time.time()
    silver = solve_silver(dots, folds)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(dots, folds)
    print(f"Gold: ")
    print_dots(solve_gold(dots, folds))
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
