
def parse():
    with open("input.txt", 'r') as raw:
        return [list(line.strip()) for line in raw.readlines()]


def part_1(map):
    trees = 0
    row = 0
    col = 0
    while row != len(map)-1:
        row += 1
        col += 3
        if col > len(map[0])-1:
            col = (col - (len(map[0])-1) - 1)
        if map[row][col] == '#':
            trees += 1
    return trees

print(part_1(parse()))