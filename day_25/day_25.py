import time


def read_input(path):
    with open(path, "r") as file:
        return [[x for x in line.strip()] for line in file.readlines()]


def solve_silver(puzzle):
    steps = 0
    row_length = len(puzzle[0])
    col_length = len(puzzle)
    while True:
        updated = 0
        update = set()
        for r, row in enumerate(puzzle):
            for c, entry in enumerate(row):
                if entry == ">" and puzzle[r][(c + 1) % row_length] == ".":
                    update.add((r, c))

        updated += len(update)
        for r, c in update:
            puzzle[r][c] = "."
            puzzle[r][(c + 1) % row_length] = ">"

        update = set()
        for r, row in enumerate(puzzle):
            for c, entry in enumerate(row):
                if entry == "v" and puzzle[(r + 1) % col_length][c] == ".":
                    update.add((r, c))

        updated += len(update)
        for r, c in update:
            puzzle[r][c] = "."
            puzzle[(r + 1) % col_length][c] = "v"

        steps += 1
        if updated == 0:
            break

    return steps


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time()-start}\n")


if __name__ == "__main__":
    main()
