import numpy as np


# Getting visible seat states from a specific seat.
def check_adjacent_seats(seats, row, column):
    seat_state = {'L': [],
                  '#': []}
    try:
        state = seats[row + 1][column]
        seat_state[state].append('down')
    except IndexError:
        pass
    except KeyError:
        pass
    try:
        state = seats[row + 1][column + 1]
        seat_state[state].append('down_diagonal_right')
    except IndexError:
        pass
    except KeyError:
        pass
    if column - 1 >= 0:
        try:
            state = seats[row + 1][column - 1]
            seat_state[state].append('down_diagonal_left')
        except IndexError:
            pass
        except KeyError:
            pass
    try:
        state = seats[row][column + 1]
        seat_state[state].append('right')
    except IndexError:
        pass
    except KeyError:
        pass
    if column - 1 >= 0:
        try:
            state = seats[row][column - 1]
            seat_state[state].append('left')
        except IndexError:
            pass
        except KeyError:
            pass
    if row - 1 >= 0:
        try:
            state = seats[row - 1][column]
            seat_state[state].append('up')
        except IndexError:
            pass
        except KeyError:
            pass
    if row - 1 >= 0:
        try:
            state = seats[row - 1][column + 1]
            seat_state[state].append('up_diagonal_right')
        except IndexError:
            pass
        except KeyError:
            pass
    if (row - 1 >= 0) & (column - 1 >= 0):
        try:
            state = seats[row - 1][column - 1]
            seat_state[state].append('up_diagonal_left')
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
    count = 0
    while running:
        count += 1
        changing_state = False
        for row in range(len(seats)):
            for column in range(len(seats[0])):

                if previous_seats[row][column] == 'L':
                    seat_state = check_adjacent_seats(previous_seats, row, column)
                    if len(seat_state['#']) == 0:
                        seats[row][column] = '#'
                        changing_state = True

                elif previous_seats[row][column] == '#':
                    seat_state = check_adjacent_seats(previous_seats, row, column)
                    if len(seat_state['#']) >= 4:
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
