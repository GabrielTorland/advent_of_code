import os
import numpy as np

def remove_errors(nearby_tickets, valid_numbers):
    errors = np.array()
    for index_0 in range(len(nearby_tickets)):
        if len(nearby_tickets[index_0]) == 0:
            errors.add(index_0)
        for index_1 in range(len(nearby_tickets[index_0])):
            try:
                test = valid_numbers[int(nearby_tickets[index_0][index_1])]
            except KeyError:
                errors.add(index_0)
                break

    return np.delete(nearby_tickets, errors)


def main():

    valid_numbers = {}
    my_ticket = []
    nearby_tickets = []
    space = 0
    with open(os.path.abspath('input.txt'), 'r') as raw:
        for line in raw:
            if line == '\n':
                space += 1

            if space == 0:
                temp = line.strip().split()
                for index, part in enumerate(temp):
                    if any(map(str.isdigit, part)):
                        t = part.split('-')
                        for i in range(int(t[1])-int(t[0])):
                            valid_numbers[int(t[0]) + i] = " ".join(temp[:index])
            elif space == 1:
                temp = line.strip().split(",")
                for part in temp:
                    if part.isdigit():
                        my_ticket.append(part)
            else:
                temp = line.strip().split(",")
                nearby_ticket = []
                for part in temp:
                    if part.isdigit():
                        nearby_ticket.append(part)
                nearby_tickets.append(nearby_ticket)
    nearby_tickets = remove_errors(np.asarray(nearby_tickets), valid_numbers)
    print()


if __name__ == "__main__":
    main()