import time

letters = {"a", "b", "c", "d", "e", "f", "g"}
length_mappings = {2: [1], 3: [7], 4: [4], 7: [8], 5: [2, 3, 5], 6: [0, 6, 9]}
section_mappings = {
    0: {0, 1, 2, 4, 5, 6},
    1: {2, 5},
    2: {0, 2, 3, 4, 6},
    3: {0, 2, 3, 5, 6},
    4: {1, 2, 3, 5},
    5: {0, 1, 3, 5, 6},
    6: {0, 1, 3, 4, 5, 6},
    7: {0, 2, 5},
    8: {0, 1, 2, 3, 4, 5, 6},
    9: {0, 1, 2, 3, 5, 6},
}


def read_input(path):
    entries = []

    with open(path, "r") as file:
        for line in file.readlines():
            patterns, output = line.strip().split(" | ")

            entries.append(
                {"patterns": patterns.split(" "), "output": output.split(" ")}
            )

    return entries


def solve_silver(puzzle):
    count = 0
    for entry in puzzle:
        for value in entry["output"]:
            if len(value) in {2, 3, 4, 7}:
                count += 1

    return count


def constrain(value, sections):
    length = len(value)
    for digit in length_mappings[length]:
        digit_sections = section_mappings[digit]
        tmp = [x for x in sections]

        for section in digit_sections:
            tmp[section] = tmp[section] & value

        for section in {0, 1, 2, 3, 4, 5, 6} - digit_sections:
            tmp[section] = tmp[section] - value

        singletons = [frozenset(x) for x in tmp if len(x) == 1]
        if set() not in tmp and len(set(singletons)) == len(singletons):
            return tmp

    return None


def solve_gold(puzzle):
    results = []

    for entry in puzzle:
        known_patterns = set(
            [frozenset(x) for x in entry["patterns"] if len(x) in {2, 3, 4, 7}]
        )
        unknown_patterns = set(
            [frozenset(x) for x in entry["patterns"] if x not in known_patterns]
        )

        sections = [letters for _ in range(len(letters))]

        for value in known_patterns:
            sections = constrain(value, sections)

        for value in unknown_patterns:
            sections = constrain(value, sections)

        digit_sections = {}

        for digit in section_mappings:
            digit_sections[digit] = set(
                [list(sections[section]).pop() for section in section_mappings[digit]]
            )

        result = ""
        for output in entry["output"]:
            for digit in digit_sections:
                if set(output) == digit_sections[digit]:
                    result += str(digit)

        results.append(result)

    return sum([int(x) for x in results])


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
