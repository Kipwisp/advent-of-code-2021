import time
import math
from collections import defaultdict

weight_map = {"A": 1, "B": 10, "C": 100, "D": 1000}
outside = {(1, 3), (1, 5), (1, 7), (1, 9)}
hall = {
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (1, 8),
    (1, 9),
    (1, 10),
    (1, 11),
}


def create_graph(lines):
    state = set()
    edges = defaultdict(list)
    for r, line in enumerate(lines[1:-1], 1):
        for c, char in enumerate(line[1:-1], 1):
            if char in {"#", " "}:
                continue

            adjacent = {
                (r + 1, c),
                (r - 1, c),
                (r, c + 1),
                (r, c - 1),
            }

            for adj in adjacent:
                if lines[adj[0]][adj[1]] not in {"#", " "}:
                    edges[(r, c)].append(adj)

            if char != ".":
                state.add(((r, c), (char, 0)))

    return state, edges


def read_input(path):
    part_2 = ["  #D#C#B#A#", "  #D#B#A#C#"]
    with open(path, "r") as file:
        lines = file.readlines()
        part_1 = create_graph(lines)

        lines = lines[:3] + part_2 + lines[3:]
        part_2 = create_graph(lines)

    return part_1, part_2


def print_state(state):
    output = [
        list("#############"),
        list("#...........#"),
        list("###.#.#.#.###"),
        list("  #.#.#.#.#"),
        list("  #.#.#.#.#"),
        list("  #.#.#.#.#"),
        list("  #########"),
    ]

    for vertex, amphi in state:
        r, c = vertex
        output[r][c] = amphi[0]

    for row in output:
        print("".join(row))


def get_amphi_at_location(state, vertex):
    for x, amphi in state:
        if x == vertex:
            return amphi[0]

    return None


step_cost_memo = {}


def step_cost(edges, state, source, to):
    stack = [(source, 0)]
    visited = set(source)

    key = state
    if (key, source, to) in step_cost_memo:
        return step_cost_memo[(key, source, to)]
    while len(stack) > 0:
        current, cost = stack.pop()

        if current == to:
            step_cost_memo[(key, source, to)] = cost
            return cost
        for adj in edges[current]:
            if adj not in state and adj not in visited:
                visited.add(adj)
                stack.append((adj, cost + 1))

    step_cost_memo[(key, source, to)] = math.inf
    return math.inf


def get_possible_moves(room_mapping, vertices, edges, current):
    vertex, amphi = current
    type, moves = amphi

    room = room_mapping[type]
    if vertex in room:
        burrow_count = 0
        for v in room[room.index(vertex) :]:
            if get_amphi_at_location(vertices, v) == type:
                burrow_count += 1

        if burrow_count == len(room) - room.index(vertex):
            return []

    moves += 1

    if moves > 2:
        return []

    possible = hall - outside
    occupied = frozenset(v for v, _ in vertices)
    possible = possible - occupied

    spot_in_room = None
    for spot in reversed(room):
        other = get_amphi_at_location(vertices, spot)
        if other is None:
            spot_in_room = spot
            break
        if other != type:
            break

    if spot_in_room:
        possible = possible | {spot_in_room}

    if moves > 1:
        possible = possible - hall

    costs = {}
    blocked = set()
    for a in possible:
        steps = step_cost(edges, occupied, vertex, a)
        if steps == math.inf:
            blocked.add(a)
        else:
            costs[a] = steps * weight_map[type]

    possible = possible - blocked

    result = []
    for adj in possible:
        result.append(((vertex, adj), (type, moves), costs[adj]))

    return result


def move(state, source, to, amphi):
    state = {x for x in state}

    state.remove((source, (amphi[0], amphi[1] - 1)))
    state.add((to, amphi))

    return frozenset(state)


def minimize(state):
    result = set()

    if state:
        for vertex, amphi in state:
            result.add((vertex, amphi[0]))

        return frozenset(result)
    else:
        return None


memo = {}


def dfs(goal, room_mapping, state, edges):
    destination, weight = state
    if minimize(destination) == goal:
        return weight

    result = []
    for vertex in destination:
        moves = get_possible_moves(room_mapping, destination, edges, vertex)
        for action, amphi, action_cost in moves:
            new_state = move(destination, *action, amphi)

            key = new_state
            if key in memo:
                result.append(memo[key])
            else:
                cost = weight + action_cost
                path_cost = dfs(
                    goal,
                    room_mapping,
                    (
                        new_state,
                        cost,
                    ),
                    edges,
                )
                result.append(path_cost)

    if result:
        memo[destination] = min(result)
        return min(result)
    else:
        memo[destination] = math.inf
        return math.inf


def solve_silver(vertices, edges):
    goal = {
        ((2, 3), "A"),
        ((2, 5), "B"),
        ((2, 7), "C"),
        ((2, 9), "D"),
        ((3, 3), "A"),
        ((3, 5), "B"),
        ((3, 7), "C"),
        ((3, 9), "D"),
    }
    room_mapping = {
        "A": [(2, 3), (3, 3)],
        "B": [(2, 5), (3, 5)],
        "C": [(2, 7), (3, 7)],
        "D": [(2, 9), (3, 9)],
    }
    start = frozenset(vertices)
    return dfs(goal, room_mapping, (start, 0), edges)


def solve_gold(vertices, edges):
    goal = {
        ((2, 3), "A"),
        ((2, 5), "B"),
        ((2, 7), "C"),
        ((2, 9), "D"),
        ((3, 3), "A"),
        ((3, 5), "B"),
        ((3, 7), "C"),
        ((3, 9), "D"),
        ((4, 3), "A"),
        ((4, 5), "B"),
        ((4, 7), "C"),
        ((4, 9), "D"),
        ((5, 3), "A"),
        ((5, 5), "B"),
        ((5, 7), "C"),
        ((5, 9), "D"),
    }
    room_mapping = {
        "A": [(2, 3), (3, 3), (4, 3), (5, 3)],
        "B": [(2, 5), (3, 5), (4, 5), (5, 5)],
        "C": [(2, 7), (3, 7), (4, 7), (5, 7)],
        "D": [(2, 9), (3, 9), (4, 9), (5, 9)],
    }
    start = frozenset(vertices)
    return dfs(goal, room_mapping, (start, 0), edges)


def main():
    path = "input.txt"
    part_1, part_2 = read_input(path)

    start = time.time()
    print(f"Silver: {solve_silver(*part_1)}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    print(f"Gold: {solve_gold(*part_2)}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
