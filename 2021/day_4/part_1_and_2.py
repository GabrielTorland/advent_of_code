
BOARD_X = 5
BOARD_Y = 5


def read_numbers(raw):
    numbers = list()
    for i in range(len(raw)):
        if raw[i] == '\n':
            return numbers, i + 1
        else:
            numbers += raw[i].strip().split(',')
    return


def read_boards(raw, index):
    # Init
    boards = list()
    board_lookup = dict()
    board = list()
    board_index = 0
    board_lookup[board_index] = dict()
    length = len(raw) - index
    x = 0

    for i in range(length)[index::]:
        if raw[i] == '\n':
            boards.append(board)
            x = 0
            if i != length - 1:
                board = list()
                board_index += 1
                board_lookup[board_index] = dict()
        else:
            numbs = raw[i].strip().split()
            board.append(numbs)
            for y, numb in enumerate(numbs):
                board_lookup[board_index][numb] = (False, (x, y))  # Marked state and x, y coordinates.
            x += 1

    return boards, board_lookup, board_index


def read_input():
    with open("input.txt", 'r') as raw:
        lines = raw.readlines()
        numbers, index = read_numbers(lines)
        boards, board_lookup, board_index = read_boards(lines, index)
    return numbers, boards, board_lookup, board_index


def bingo(board, board_lookup, index, coordinates):
    not_bingo_count = 0
    for rows in range(BOARD_X):
        numb = board[rows][coordinates[1]]
        if not board_lookup[index][numb][0]:
            not_bingo_count += 1
            break
    for cols in range(BOARD_Y):
        numb = board[coordinates[0]][cols]
        if not board_lookup[index][numb][0]:
            not_bingo_count += 1
            break
    return False if not_bingo_count == 2 else True


def main():
    numbers, boards, board_lookup, board_index = read_input()
    winning_boards = list()
    boards_won = set()

    # Game starts
    for bingo_round, numb in enumerate(numbers):
        for i in range(board_index + 1):
            try:
                state, coordinates = board_lookup[i][numb]
                board_lookup[i][numb] = (True, coordinates)
                if (i not in boards_won) and bingo(boards[i], board_lookup, i, coordinates):
                    winning_boards.append(i)
            except:
                continue
        if len(winning_boards) > 0:
            print(f"The first winning board is at round {bingo_round + 1} with last number {numb}.")
            for board in winning_boards:
                resulting_sum = 0
                for x in range(BOARD_X):
                    for y in range(BOARD_Y):
                        num = boards[board][x][y]
                        if not board_lookup[board][num][0]:
                            resulting_sum += int(num)
                print(f"Final score for the first winning board is {resulting_sum * int(numb)}")
            for b in winning_boards:
                boards_won.add(b)
            winning_boards = list()


if __name__ == "__main__":
    main()
