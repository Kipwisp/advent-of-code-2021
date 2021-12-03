import time


def read_input(path):
    result = []

    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]

    return result


def solve_silver(puzzle):
    gamma = ""
    epsilon = ""
    bits_length = len(puzzle[0])

    counts = []
    for i in range(bits_length):
        counts.append(len([x for x in puzzle if x[i] == "1"]))

    for i in range(bits_length):
        ones = counts[i]
        zeroes = len(puzzle) - ones
        if zeroes > ones:
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"

    return int(gamma, 2) * int(epsilon, 2)


def get_rating(puzzle, condition):
    ratings = [x for x in puzzle]
    bits_length = len(puzzle[0])

    for i in range(bits_length):
        counts = {
            "0": len([x for x in ratings if x[i] == "0"]),
            "1": len([x for x in ratings if x[i] == "1"]),
        }

        j = 0
        while j < len(ratings):
            bit = ratings[j][i]
            zeroes, ones = counts["0"], counts["1"]
            if (
                condition(zeroes, ones)
                and bit == "1"
                or not condition(zeroes, ones)
                and bit == "0"
            ):
                ratings.pop(j)
                j -= 1

            if len(ratings) == 1:
                return ratings.pop()

            j += 1


def solve_gold(puzzle):
    oxygen_rating = get_rating(puzzle, lambda x, y: x > y)
    scrubber_rating = get_rating(puzzle, lambda x, y: x <= y)

    return int(oxygen_rating, 2) * int(scrubber_rating, 2)


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
