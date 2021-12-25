import time


def read_input(path):
    result = []
    with open(path, "r") as file:
        for line in file.readlines():
            instruction, *args = line.strip().split(" ")

            result.append([instruction, args])

    return result


def get_value(register, arg):
    if arg in register:
        return register[arg]

    return int(arg)


def test_number(puzzle, number):
    register = {"w": 0, "x": 0, "y": 0, "z": 0}
    inp = number

    for i, item in enumerate(puzzle):
        instruction, args = item
        store = args[0]
        args = [get_value(register, x) for x in args]
        if instruction == "inp":
            register[store] = inp.pop(0)
        elif instruction == "add":
            register[store] = args[0] + args[1]
        elif instruction == "mul":
            register[store] = args[0] * args[1]
        elif instruction == "div":
            register[store] = args[0] // args[1]
        elif instruction == "mod":
            register[store] = args[0] % args[1]
        elif instruction == "eql":
            register[store] = args[0] == args[1]

    return register["z"] == 0


def get_model_number(puzzle):
    stack = []
    biggest_number = [0] * 14
    smallest_number = [0] * 14

    index = 0
    for i, item in enumerate(puzzle):
        instruction, args = item

        if instruction == "div":
            if args[1] == "1":
                _, x = puzzle[i + 11]
                x = int(x[1])
                stack.append((x, index))
            else:
                _, x = puzzle[i + 1]
                x = int(x[1])
                y, j = stack.pop()

                difference = abs(y + x)

                if abs(x) <= y:
                    biggest_number[j] = 9 - difference
                    biggest_number[index] = 9

                    smallest_number[j] = 1
                    smallest_number[index] = 1 + difference
                else:
                    biggest_number[j] = 9
                    biggest_number[index] = 9 - difference

                    smallest_number[j] = 1 + difference
                    smallest_number[index] = 1

            index += 1

    return "".join([str(x) for x in smallest_number]), "".join(
        [str(x) for x in biggest_number]
    )


def solve_silver(puzzle):
    _, number = get_model_number(puzzle)
    return number


def solve_gold(puzzle):
    number, _ = get_model_number(puzzle)
    return number


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
