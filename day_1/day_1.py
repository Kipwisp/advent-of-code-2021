import time


def read_input(path):
    result = []

    with open(path, "r") as file:
        result = file.readlines()

        for i, line in enumerate(result):
            result[i] = int(line.strip())

    return result


def solve_silver(puzzle):
    count = 0

    for i in range(1, len(puzzle)):
        if puzzle[i] > puzzle[i - 1]:
            count += 1

    return count


def solve_gold(puzzle):
    count = 0
    window_size = 3

    for i in range(window_size, len(puzzle)):
        if sum(puzzle[i - window_size : i]) > sum(puzzle[i - window_size - 1 : i - 1]):
            count += 1

    return count


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time()-start}\n")

    start = time.time()
    gold = solve_gold(puzzle)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time()-start}\n")


if __name__ == "__main__":
    main()
