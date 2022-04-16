def get_row(seat):
    rows = (0, 127)
    for i in range(7):
        if seat[i] == 'F':
            rows = (rows[0], (rows[1] + 1 - rows[0]) / 2 + rows[0] - 1)
        else:
            rows = ((rows[1] + 1 - rows[0]) / 2 + rows[0], rows[1])
    return rows


def get_column(seat):
    columns = (0, 7)
    for i in range(3):
        if seat[i + 7] == 'R':
            columns = ((columns[1] + 1 - columns[0]) / 2 + columns[0], columns[1])
        else:
            columns = (columns[0], (columns[1] + 1 - columns[0]) / 2 + columns[0] - 1)
    return columns


def main():
    seat_data = []
    ids = []
    seats_occupied = {}

    with open('input.txt', 'r') as seat_description:
        for line in seat_description:
            seat_data.append(line.strip())
    # Part 1.
    for seat in seat_data:
        id_ = get_row(seat)[0] * 8 + get_column(seat)[0]
        seats_occupied[id_] = True
        ids.append(id_)

    print(f"The largest id is: {max(ids)}.")

    # Part 2.
    # Method one, this is probably the most efficient way to solve this.
    for id_1 in sorted(ids):
        if id_1 + 1 not in ids and id_1 + 2 in ids:
            missing = id_1 + 1
        elif id_1 - 1 not in ids and id_1 - 2 in ids:
            missing = id_1 - 1

    print(f"Your seat has id: {missing}.")

    # Method two.
    pos_empty_seats = []
    # Finding empty seats.
    for row in range(128):
        # Your seat was not in the back or front.
        if row > 4 & row < 123:
            for column in range(8):
                try:
                    test = seats_occupied[row * 8 + column]
                except:
                    try:
                        test_3 = seats_occupied[(row * 8 + column) - 1]
                        test_2 = seats_occupied[(row * 8 + column) + 1]
                        pos_empty_seats.append((row * 8 + column))
                    except:
                        continue
    print(f'Your seat has id: {pos_empty_seats}.')


if __name__ == "__main__":
    main()




