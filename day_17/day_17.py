import time
import re
import math


def read_input(path):
    with open(path, "r") as file:
        x_range, y_range = re.findall("-?[0-9]+..-?[0-9]+", file.read().strip())
        x_range = [int(e) for e in x_range.split("..")]
        y_range = [int(e) for e in y_range.split("..")]

    return x_range, y_range


def trick_shot(x_range, y_range):
    highest = -math.inf
    distinct_vels = 0
    for i in range(min(y_range), abs(min(y_range)) + 1):
        for j in range(max(x_range) + 1):
            height = 0
            x, y = 0, 0
            vel_x, vel_y = j, i
            while True:
                x += vel_x
                y += vel_y

                height = y if y > height else height

                if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                    highest = height if height > highest else highest
                    distinct_vels += 1
                    break

                if x > max(x_range) or y < min(y_range):
                    break

                vel_x -= 1 if vel_x != 0 else 0
                vel_y -= 1

    return highest, distinct_vels


def solve_silver(x_range, y_range):
    highest, _ = trick_shot(x_range, y_range)
    return highest


def solve_gold(x_range, y_range):
    _, distinct_vels = trick_shot(x_range, y_range)
    return distinct_vels


def main():
    path = "input.txt"
    x_range, y_range = read_input(path)

    start = time.time()
    silver = solve_silver(x_range, y_range)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(x_range, y_range)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
