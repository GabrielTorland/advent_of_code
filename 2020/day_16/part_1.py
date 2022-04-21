import os


def main():
    valid_numbers = {}
    my_ticket = []
    nearby_tickets = []
    space = 0
    with open(os.path.abspath('input.txt'), 'r') as raw:
        for line in raw:
            if line == '\n':
                space += 1
                continue
            if "tickets" in line:
                continue

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
                    my_ticket.append(part)
            else:
                temp = line.strip().split(",")
                nearby_ticket = []
                for part in temp:
                    nearby_ticket.append(part)
                nearby_tickets.append(nearby_ticket)

    errors = []
    for ticket in nearby_tickets:
        for number in ticket:
            try:
               test = valid_numbers[int(number)]
            except KeyError:
                errors.append(int(number))
                break
    print(sum(errors))


if __name__ == "__main__":
    main()