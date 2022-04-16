import copy
from itertools import product


def parse_input():
    with open("input.txt", 'r') as raw:
        result = list()
        for line in raw:
            iterations = line.strip()
            result.append([int(number) for number in iterations])
    return result


def main():
    flashes = 0

    data = parse_input()

    # Original flash state for every octopus.
    flashed = dict()
    for x in range(len(data)):
        for y in range(len(data[x])):
            flashed[(x, y)] = False

    depth = 1000

    for i in range(depth):
        # Flash state for current round.
        temp_flashed = copy.deepcopy(flashed)
        for x in range(len(data)):
            for y in range(len(data[x])):
                if not temp_flashed[(x, y)]:
                    data[x][y] = (data[x][y] + 1) % 10
                    if data[x][y] == 0:
                        temp_flashed[(x, y)] = True
                        flashes += 1
                        queue = [(x, y)]
                        while len(queue) != 0:
                            x_, y_ = queue.pop()
                            # Combinations without repetition to find adjacent flashes.
                            for add_x, add_y in [p for p in product([1, -1, 0], repeat=2) if p != (0, 0)]:
                                if ((x_ + add_x) in range(0, len(data))) and ((y_ + add_y) in range(len(data[x_ + add_x]))):
                                    if not temp_flashed[(x_ + add_x, y_ + add_y)]:
                                        data[x_ + add_x][y_ + add_y] = (data[x_ + add_x][y_ + add_y] + 1) % 10
                                    else:
                                        continue
                                    if data[x_ + add_x][y_ + add_y] == 0:
                                        flashes += 1
                                        temp_flashed[(x_ + add_x, y_ + add_y)] = True
                                        queue.append((x_ + add_x, y_ + add_y))
        if False not in temp_flashed.values():
            print(i+1)
            break
    print(flashes)


if __name__ == "__main__":
    main()
