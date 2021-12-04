import time


def read_input(path):
    drawing_order = []
    boards = []

    with open(path, "r") as file:
        drawing_order = [int(x) for x in file.readline().strip().split(",")]
        boards = []

        board = []
        for line in file.readlines()[1:]:
            if line == "\n":
                boards.append(board)
                board = []
            else:
                board.append(
                    [
                        {"number": int(x), "drawn": False}
                        for x in line.strip().split(" ")
                        if x != ""
                    ]
                )

        boards.append(board)

    return drawing_order, boards


def mark_board(num, board):
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c]["number"] == num:
                board[r][c]["drawn"] = True

                return len([x for x in board[r] if x["drawn"]]) == size or (
                    len([board[k][c] for k in range(size) if board[k][c]["drawn"]])
                    == size
                )


def get_winning_board(drawing_order, boards):
    for num in drawing_order:
        for board in boards:
            won = mark_board(num, board)

            if won:
                return board, num


def get_last_winning_board(drawing_order, boards):
    for num in drawing_order:
        i = 0
        while i < len(boards):
            board = boards[i]
            won = mark_board(num, board)

            if won:
                b = boards.pop(i)

                if len(boards) == 0:
                    return b, num

                i -= 1

            i += 1


def solve_silver(drawing_order, boards):
    board, last_num = get_winning_board(drawing_order, boards)

    sum = 0
    for row in board:
        for entry in row:
            if not entry["drawn"]:
                sum += entry["number"]

    return sum * last_num


def solve_gold(drawing_order, boards):
    board, last_num = get_last_winning_board(drawing_order, boards)

    sum = 0
    for row in board:
        for entry in row:
            if not entry["drawn"]:
                sum += entry["number"]

    return sum * last_num


def main():
    path = "input.txt"
    drawing_order, boards = read_input(path)

    start = time.time()
    silver = solve_silver(drawing_order, boards)
    print(f"Silver: {silver}")
    print(f"Delta: {time.time() - start}\n")

    start = time.time()
    gold = solve_gold(drawing_order, boards)
    print(f"Gold: {gold}")
    print(f"Delta: {time.time() - start}\n")


if __name__ == "__main__":
    main()
