
def parse():
    with open("input.txt", 'r') as raw:
        return [list(line.strip()) for line in raw.readlines()]


def part_2(map):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    result = 1
    for slope in slopes:
        trees = 0
        row = 0
        col = 0
        while row != len(map)-1:
            row += slope[1]
            col += slope[0]
            if col > len(map[0])-1:
                col = (col - (len(map[0])-1) - 1)
            if map[row][col] == '#':
                trees += 1
        result *= trees
    return result

print(part_2(parse()))