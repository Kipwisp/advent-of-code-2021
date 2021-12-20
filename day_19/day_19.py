import time
import numpy as np
import math

rotations = [0, math.pi / 2, math.pi, (math.pi * 3) / 2]


def read_input(path):
    result = []

    with open(path, "r") as file:
        for scanner in file.read().split("\n\n"):
            beacons = set()
            for line in scanner.split("\n")[1:]:
                beacons.add(tuple(int(x) for x in line.split(",")))

            result.append(beacons)

    return result


def rotate(point, x, y, z):
    x_matrix = np.array(
        [
            [1, 0, 0],
            [0, math.cos(x), -math.sin(x)],
            [0, math.sin(x), math.cos(x)],
        ],
        dtype=int,
    )
    y_matrix = np.array(
        [
            [math.cos(y), 0, math.sin(y)],
            [0, 1, 0],
            [-math.sin(y), 0, math.cos(y)],
        ],
        dtype=int,
    )
    z_matrix = np.array(
        [
            [math.cos(z), -math.sin(z), 0],
            [math.sin(z), math.cos(z), 0],
            [0, 0, 1],
        ],
        dtype=int,
    )

    return tuple((x_matrix @ y_matrix @ z_matrix @ point).tolist())


def find_match(scanner_1, scanner_2):
    min_matches = 12
    seen = set()
    for z_rotation in rotations:
        for x_rotation in rotations:
            for y_rotation in rotations:
                rotated = {
                    rotate(beacon, x_rotation, y_rotation, z_rotation)
                    for beacon in scanner_2
                }

                if frozenset(rotated) in seen:
                    continue

                seen.add(frozenset(rotated))

                for beacon_1 in scanner_1:
                    for beacon_2 in rotated:
                        dx = beacon_1[0] - beacon_2[0]
                        dy = beacon_1[1] - beacon_2[1]
                        dz = beacon_1[2] - beacon_2[2]

                        shifted = {(x[0] + dx, x[1] + dy, x[2] + dz) for x in rotated}

                        if len(shifted.intersection(scanner_1)) >= min_matches:
                            return shifted, (dx, dy, dz)

    return None


def solve_silver(puzzle):
    map = puzzle.pop(0)
    scanners = {(0, 0, 0)}

    while len(puzzle) > 0:
        for scanner in puzzle:
            result = find_match(map, scanner)

            if not result:
                continue

            beacons, position = result

            map.update(beacons)
            scanners.add(position)
            puzzle.remove(scanner)

            print("Found match!")
            print("Beacons found:", len(map))
            break

    return len(map), scanners


def solve_gold(puzzle):
    best = 0
    for scanner in puzzle:
        for other in puzzle:
            distance = (
                abs(scanner[0] - other[0])
                + abs(scanner[1] - other[1])
                + abs(scanner[2] - other[2])
            )
            if distance > best:
                best = distance

    return best


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    silver, positions = solve_silver(puzzle)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time()-start}\n")

    start = time.time()
    gold = solve_gold(positions)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time()-start}\n")


if __name__ == "__main__":
    main()
