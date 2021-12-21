import time
import copy


def read_input(path):
    with open(path, "r") as file:
        algorithm, image = file.read().split("\n\n")

        algorithm = "".join(line.strip() for line in algorithm)

        image = {
            (i, j): e
            for i, row in enumerate(image.split("\n"))
            for j, e in enumerate(row)
        }

    return algorithm, image


def enhance(steps, algorithm, image):
    region = set(k for k in image)
    image = set(k for k in image if image[k] == "#")
    border = "."
    for step in range(steps):
        new = set()
        seen = set()
        update = copy.deepcopy(image)
        while len(update) > 0:
            pixel = update.pop()
            seen.add(pixel)

            r, c = pixel

            adjacent = [(r + i, c + j) for i in range(-1, 2) for j in range(-1, 2)]
            index = int(
                "".join(
                    [
                        "1"
                        if adj in image or (adj not in region and border == "#")
                        else "0"
                        for adj in adjacent
                    ]
                ),
                2,
            )

            if algorithm[index] == "#":
                new.add(pixel)

            if pixel in region:
                update.update(set(adjacent) - seen)

        image = new
        region = seen
        border = algorithm[-1] if step % 2 == 1 and border == "#" else algorithm[0]

    return len(image)


def solve_silver(algorithm, image):
    return enhance(2, algorithm, image)


def solve_gold(algorithm, image):
    return enhance(50, algorithm, image)


def main():
    path = "input.txt"
    algorithm, image = read_input(path)

    start = time.time()
    silver = solve_silver(algorithm, image)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time()-start}\n")

    start = time.time()
    gold = solve_gold(algorithm, image)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time()-start}\n")


if __name__ == "__main__":
    main()
