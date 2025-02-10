from collections import defaultdict

def parse(input_file = "input.txt"):
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    antennas = defaultdict(list)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '.':
                continue
            antennas[char].append((i, j))
    y_max = len(lines)
    x_max = len(lines[0])
    return antennas, y_max, x_max


def get_antinodes(antennas, x_max, y_max):
    antinodes = set()
    for antenna, coords in antennas.items():
        for i, coord1 in enumerate(coords):
            for coord2 in coords[i+1:]:
                y1, x1 = coord1
                y2, x2 = coord2
                x_diff = abs(x1 - x2)
                y_diff = abs(y1 - y2)

                new_x = x1 + x_diff if x1 > x2 else x1 - x_diff
                new_y = y1 + y_diff if y1 > y2 else y1 - y_diff
                if new_x >= 0 and new_x < x_max and new_y >= 0 and new_y < y_max:
                    antinodes.add((new_y, new_x))

                new_x = x2 + x_diff if x2 > x1 else x2 - x_diff
                new_y = y2 + y_diff if y2 > y1 else y2 - y_diff
                if new_x >= 0 and new_x < x_max and new_y >= 0 and new_y < y_max:
                    antinodes.add((new_y, new_x))
    return antinodes

def get_antinodes_updated(antennas, x_max, y_max):
    antinodes = set()
    for antenna, coords in antennas.items():
        for i, coord1 in enumerate(coords):
            for coord2 in coords[i+1:]:
                y1, x1 = coord1
                y2, x2 = coord2
                x_diff = abs(x1 - x2)
                y_diff = abs(y1 - y2)

                x_current, y_current = x1, y1
                while x_current >= 0 and x_current < x_max and y_current >= 0 and y_current < y_max:
                    antinodes.add((y_current, x_current))
                    x_current = x_current + x_diff if x1 > x2 else x_current - x_diff
                    y_current = y_current + y_diff if y1 > y2 else y_current - y_diff

                x_current, y_current = x2, y2
                while x_current >= 0 and x_current < x_max and y_current >= 0 and y_current < y_max:
                    antinodes.add((y_current, x_current))
                    x_current = x_current + x_diff if x2 > x1 else x_current - x_diff
                    y_current = y_current + y_diff if y2 > y1 else y_current - y_diff
    return antinodes

if __name__ == "__main__":
    antennas, y_max, x_max = parse()
    antinodes = get_antinodes(antennas, x_max, y_max)
    print("Part 1: ", len(antinodes))
    antinodes = get_antinodes_updated(antennas, x_max, y_max)

    for i in range(y_max):
        for j in range(x_max):
            if (i, j) in antennas['A']:
                print("A", end="")
            elif (i, j) in antennas['0']:
                print("0", end="")
            elif (i, j) in antinodes:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print("Part 2: ", len(antinodes))