import time
import math
from collections import defaultdict


def read_input(path):
    edges = defaultdict(lambda: set())

    with open(path, "r") as file:
        for line in file.readlines():
            a, b = line.strip().split("-")
            edges[a].add(b)
            edges[b].add(a)

    return edges


def dfs(edges, part_2=False):
    start = "start"
    stack = [(None, start, set(), False)]
    paths = 0

    while len(stack) > 0:
        _, destination, visited, smallVisitedTwice = stack.pop()
        if destination == "end":
            paths += 1
            continue

        visited = visited.copy()
        visited.add(destination)

        for adj in edges[destination]:
            if adj[0].isupper() or adj not in visited:
                stack.append((destination, adj, visited, smallVisitedTwice))
            elif not smallVisitedTwice and adj != "start" and part_2:
                stack.append((destination, adj, visited, True))

    return paths


def solve_silver(edges):
    return dfs(edges)


def solve_gold(edges):
    return dfs(edges, True)


def main():
    path = "input.txt"
    edges = read_input(path)

    start = time.time()
    silver = solve_silver(edges)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(edges)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
