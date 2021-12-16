import time
import math


class PriorityQueue:
    def __init__(self, collection):
        self.queue = []
        self.append(*collection)

    def pop(self):
        top_priority = math.inf
        index = -1
        for i, item in enumerate(self.queue):
            _, priority = item
            if priority < top_priority:
                top_priority = priority
                index = i

        return self.queue.pop(index)[0]

    def append(self, item, priority):
        self.queue.append((item, priority))

    def __len__(self):
        return len(self.queue)


def read_input(path):
    with open(path, "r") as file:
        return [[int(x) for x in line.strip()] for line in file.readlines()]


def expand_cave(puzzle):
    result = []

    for i in range(5):
        for row in puzzle:
            r = []
            for j in range(5):
                for entry in row:
                    next = entry + i + j
                    r.append(next if next < 10 else next - 9)

            result.append(r)

    return result


def heuristic(node, goal):
    return math.sqrt((goal[0] - node[0]) ** 2 + (goal[1] - node[1]) ** 2)


def dijkstra(puzzle):
    start = (0, 0)
    end = (len(puzzle) - 1, len(puzzle[0]) - 1)
    queue = PriorityQueue(((None, start, 0), 0))
    backpointers = {}
    visited = {start}

    while len(queue) > 0:
        source, destination, weight = queue.pop()

        backpointers[destination] = source

        if destination == end:
            break

        r, c = destination
        adjacent = [
            (r + 1, c),
            (r - 1, c),
            (r, c + 1),
            (r, c - 1),
        ]

        for adj in adjacent:
            if (
                adj not in visited
                and 0 <= adj[0] < len(puzzle)
                and 0 <= adj[1] < len(puzzle[0])
            ):
                visited.add(adj)
                cost = weight + puzzle[adj[0]][adj[1]]
                queue.append(
                    (destination, adj, cost),
                    cost,
                )

    total_risk = 0
    current = end
    while backpointers[current]:
        total_risk += puzzle[current[0]][current[1]]
        current = backpointers[current]

    return total_risk


def solve_silver(puzzle):
    return dijkstra(puzzle)


def solve_gold(puzzle):
    return dijkstra(puzzle)


def main():
    path = "input.txt"
    puzzle = read_input(path)

    start = time.time()
    print(f"Silver: {solve_silver(puzzle)}")
    print(f"Delta: {time.time() - start}\n")

    puzzle = expand_cave(puzzle)

    start = time.time()
    print(f"Gold: {solve_gold(puzzle)}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
