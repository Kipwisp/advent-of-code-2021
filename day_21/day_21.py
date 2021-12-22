import time


def read_input(path):
    with open(path, "r") as file:
        return [int(line.strip().split(": ")[-1]) for line in file.readlines()]


def roll_practice_dice(die, position):
    return (position + 3 * die + 2) % 10 + 1, (die + 2) % 100 + 1


def solve_silver(puzzle):
    winning_score = 1000
    p1_pos, p2_pos = puzzle
    p1_score, p2_score = 0, 0

    die = 1
    rolls = 0

    while True:
        p1_pos, die = roll_practice_dice(die, p1_pos)
        rolls += 3

        p1_score += p1_pos
        if p1_score >= winning_score:
            break

        p2_pos, die = roll_practice_dice(die, p2_pos)
        rolls += 3

        p2_score += p2_pos
        if p2_score >= winning_score:
            break

    return min((p1_score, p2_score)) * rolls


outcomes = [i + j + k for i in range(1, 4) for j in range(1, 4) for k in range(1, 4)]


def get_next_state(state, dice):
    p1_score, p2_score, p1_pos, p2_pos, player_turn = state
    pos = p1_pos if player_turn == 0 else p2_pos
    pos = (pos + dice - 1) % 10 + 1
    next_turn = (player_turn + 1) % 2
    return (
        (
            p1_score + pos,
            p2_score,
            pos,
            p2_pos,
            next_turn,
        )
        if player_turn == 0
        else (p1_score, p2_score + pos, p1_pos, pos, next_turn)
    )


def game(state, memo):
    winning_score = 21
    wins = [0, 0]

    p1_score, p2_score = state[:2]
    if p1_score >= winning_score:
        return [1, 0]
    elif p2_score >= winning_score:
        return [0, 1]

    for dice in outcomes:
        new_state = get_next_state(state, dice)
        if new_state in memo:
            wins = [sum((x, y)) for x, y in zip(wins, memo[new_state])]
        else:
            result = game(new_state, memo)
            wins = [sum((x, y)) for x, y in zip(wins, result)]

    memo[state] = wins
    return wins


def solve_gold(puzzle):
    p1_pos, p2_pos = puzzle
    memo = {}
    wins = game((0, 0, p1_pos, p2_pos, 0), memo)
    return max(wins)


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
