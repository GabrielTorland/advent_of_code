import math


def parse_input():
    with open("input.txt", 'r') as raw:
        rows = -math.inf
        cols = -math.inf
        dots = set()
        splits = list()
        split = False
        for line in raw:
            if line == '\n':
                split = True
                continue
            temp = line.strip()

            if split:
                fold = temp.split(' ').pop()
                splits.append([fold[0], int(''.join(str(char) for char in list(fold)[2::]))])
            else:
                data = temp.split(',')
                x = int(data[0])
                if x > cols:
                    cols = x
                y = int(data[1])
                if y > rows:
                    rows = y
                dots.add((x, y))
    return dots, splits, rows, cols


def print_as_grid(dots, rows, cols):
    for row in range(rows):
        line = ""
        for col in range(cols):

            if (col, row) in dots:
                line += '#'
            else:
                line += '.'
        print(line)
    print()


def main():
    dots, splits, rows, cols = parse_input()
    print(len(dots))
    for split in splits:
        prev_dots = dots.copy()
        if split[0] == 'y':
            rows = split[1]
            for dot in prev_dots:
                if dot[1] > split[1]:
                    dots.add((dot[0], 2 * split[1] - dot[1]))
                    dots.remove(dot)
        else:
            cols = split[1]
            for dot in prev_dots:
                if dot[0] > split[1]:
                    dots.add((2 * split[1] - dot[0], dot[1]))
                    dots.remove(dot)
        print(len(dots))
        print_as_grid(dots, rows, cols)


if __name__ == "__main__":
    main()
