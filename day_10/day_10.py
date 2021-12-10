import time
from functools import reduce


def read_input(path):
    result = []

    with open(path, "r") as file:
        return [x.strip() for x in file.readlines()]


def solve_silver(puzzle):
    chunks = {"(": ")", "[": "]", "{": "}", "<": ">"}
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    corrupted_lines = set()

    for i, line in enumerate(puzzle):
        stack = []
        for char in line:
            if char in chunks:
                stack.append(char)
            elif chunks[stack[-1]] != char:
                score += points[char]
                corrupted_lines.add(i)
                break
            else:
                stack.pop()

    return score, corrupted_lines


def solve_gold(puzzle, corrupted_lines):
    chunks = {"(": ")", "[": "]", "{": "}", "<": ">"}
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    result = []

    puzzle = [x for i, x in enumerate(puzzle) if i not in corrupted_lines]

    for line in puzzle:
        stack = []
        for char in line:
            stack.append(char) if char in chunks else stack.pop()

        result.append(
            reduce(lambda acc, char: acc * 5 + points[chunks[char]], reversed(stack), 0)
        )

    return sorted(result)[len(result) // 2]


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver, corrupted_lines = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(puzzle, corrupted_lines)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
