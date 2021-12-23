import time
import re


def read_input(path):
    result = []
    with open(path, "r") as file:
        for line in file.readlines():
            r = []
            command = line.split(" ")[0] == "on"
            r.append(command)
            bounds = re.findall("-?[0-9]+..-?[0-9]+", line.strip())
            r.append(
                tuple(
                    (int(lower), int(upper))
                    for bound in bounds
                    for lower, upper in [bound.split("..")]
                )
            )

            result.append(r)

    return result


def intersects(a, b):
    if a[1] < b[0] or b[1] < a[0]:
        return None

    return max(a[0], b[0]), min(a[1], b[1])


def get_volume(cube):
    x, y, z = cube
    return (abs(x[1] - x[0]) + 1) * (abs(y[1] - y[0]) + 1) * (abs(z[1] - z[0]) + 1)


def reboot(puzzle, part_2=False):
    intersections = []
    cubes = 0
    for command, bound in puzzle:
        x, y, z = bound
        if not part_2 and (x[0] < -50 or x[0] > 50):
            continue

        subintersections = []
        for subcommand, intersection in intersections:
            a, b, c = intersection
            x_i = intersects(a, x)
            y_i = intersects(b, y)
            z_i = intersects(c, z)

            if None not in (x_i, y_i, z_i):
                subintersections.append((not subcommand, (x_i, y_i, z_i)))
                if subcommand:
                    cubes -= get_volume((x_i, y_i, z_i))
                else:
                    cubes += get_volume((x_i, y_i, z_i))

        intersections.extend(subintersections)
        if command:
            intersections.append((command, bound))
            cubes += get_volume(bound)

    return cubes


def solve_silver(puzzle):
    return reboot(puzzle)


def solve_gold(puzzle):
    return reboot(puzzle, part_2=True)


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
