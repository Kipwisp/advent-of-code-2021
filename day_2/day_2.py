import time


def read_input(path):
    result = []

    with open(path, "r") as file:
        return [
            [value[0], int(value[1])]
            for value in [line.split() for line in file.readlines()]
        ]


def solve_silver(puzzle):
    depth = 0
    horizontal = 0

    for command, value in puzzle:
        if command == "forward":
            horizontal += value
        elif command == "down":
            depth += value
        elif command == "up":
            depth -= value

    return depth * horizontal


def solve_gold(puzzle):
    depth = 0
    horizontal = 0
    aim = 0

    for command, value in puzzle:
        if command == "forward":
            horizontal += value
            depth += aim * value
        elif command == "down":
            aim += value
        elif command == "up":
            aim -= value

    return depth * horizontal


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
