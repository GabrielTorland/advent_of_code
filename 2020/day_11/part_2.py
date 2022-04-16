import numpy as np


# Getting visible seat states from a specific seat.
def check_adjacent_seats(seats, row, column, rows, columns):
    seat_state = {'L': [],
                  '#': []}

    for i in range(rows - row + 1)[1:]:
        try:
            state = seats[row + i][column]
            seat_state[state].append((row + i, column))
            break
        except IndexError:
            pass
        except KeyError:
            pass
    for i in range(rows - row + 1)[1:]:
        try:
            state = seats[row + i][column + i]
            seat_state[state].append((row + i, column + i))
            break
        except IndexError:
            pass
        except KeyError:
            pass

    for i in range(rows - row + 1)[1:]:
        if column - i >= 0:
            try:
                state = seats[row + i][column - i]
                seat_state[state].append((row + i, column - i))
                break
            except IndexError:
                pass
            except KeyError:
                pass
    for i in range(columns - column + 1)[1:]:
        try:
            state = seats[row][column + i]
            seat_state[state].append((row, column + i))
            break
        except IndexError:
            pass
        except KeyError:
            pass

    for i in range(column + 1)[1:]:
        if column - i >= 0:
            try:
                state = seats[row][column - i]
                seat_state[state].append((row, column - i))
                break
            except IndexError:
                pass
            except KeyError:
                pass
    for i in range(row + 1)[1:]:
        if row - i >= 0:
            try:
                state = seats[row - i][column]
                seat_state[state].append((row - i, column))
                break
            except IndexError:
                pass
            except KeyError:
                pass

    for i in range(row + 1)[1:]:
        if row - i >= 0:
            try:
                state = seats[row - i][column + i]
                seat_state[state].append((row - i, column + i))
                break
            except IndexError:
                pass
            except KeyError:
                pass

    for i in range(row + 1)[1:]:
        if (row - i >= 0) & (column - i >= 0):
            try:
                state = seats[row - i][column - i]
                seat_state[state].append((row - i, column - i))
                break
            except IndexError:
                pass
            except KeyError:
                pass
    return seat_state


def main():
    seats = []
    with open('input', 'r') as raw:
        for line in raw:
            seats.append(list(line.strip()))

    # Using numpy array instead of list because of efficiency needed.
    previous_seats = np.asarray(seats)
    seats = previous_seats.copy()
    running = True
    rows = len(seats)
    columns = len(seats[0])
    count = 0
    while running:
        count += 1
        changing_state = False
        for row in range(rows):
            for column in range(columns):

                if previous_seats[row][column] == 'L':
                    seat_state = check_adjacent_seats(previous_seats, row, column, rows, columns)
                    if len(seat_state['#']) == 0:
                        seats[row][column] = '#'
                        changing_state = True

                elif previous_seats[row][column] == '#':
                    seat_state = check_adjacent_seats(previous_seats, row, column, rows, columns)
                    if len(seat_state['#']) >= 5:
                        seats[row][column] = 'L'
                        changing_state = True

        if changing_state is False:
            occupied_seats = 0
            for seat in seats.flatten():
                if seat == '#':
                    occupied_seats += 1
            print(f"{occupied_seats} seats end up occupied after {count} changes.")
            running = False
        else:
            previous_seats = seats.copy()


if __name__ == "__main__":
    main()