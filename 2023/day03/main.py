import re
import numpy as np

def parse(input):
    return open(input).read().splitlines()

def find_neighbors(data, x1, x2, y):
    # Extract all the entries around the number, i.e. the neighbors
    # Note that this could have been done more efficiently. However, this approach is taken to improve readability.
    above = data[y-1][x1:x2] if y-1 >= 0 else ''
    below = data[y+1][x1:x2] if y+1 < len(data) else ''
    left = data[y][x1-1] if x1-1 >= 0 else ''
    right = data[y][x2] if x2 < len(data[y]) else ''
    top_left_corner = data[y-1][x1-1] if y-1 >= 0 and x1-1 >= 0 else ''
    bottom_left_corner = data[y+1][x1-1] if y+1 < len(data) and x1-1 >= 0 else ''
    top_right_corner = data[y-1][x2] if y-1 >= 0 and x2 < len(data[y]) else ''
    bottom_right_corner = data[y+1][x2] if y+1 < len(data) and x2 < len(data[y]) else ''

    return top_left_corner + above + top_right_corner + '.' + left + '.' + right + '.' + bottom_left_corner + below + bottom_right_corner

def has_adjacent_symbol(data, symbol, pos):
    x1, x2, y = pos
    pattern = re.compile(symbol)
    neighbors = find_neighbors(data, x1, x2, y)
    return pattern.findall(neighbors) 

def find_entire_numbers(data, x, y):
    neighbors = find_neighbors(data, x, x+1, y)
    numbers = []
    for number in re.finditer(r'(\d+)', neighbors):
        x_s, x_e = number.span()
        i = x_s
        x1, x2, y1 = x, x, y
        # The index change is the delta to get the correct index in the data
        index_change = {0: (-1, -1), 1: (0, -1), 2: (1, -1), 4: (-1, 0), 6: (1, 0), 8: (-1, 1), 9: (0, 1), 10: (1, 1)}
        # Adding the delta to get the correct index in the data
        x1 += index_change[i][0]
        x2 += index_change[i][0]
        y1 += index_change[i][1]

        while x1-1 >= 0 and data[y1][x1-1].isdigit():
            x1 -= 1
        while x2 < len(data[y1]) and data[y1][x2].isdigit():
            x2 += 1
        numbers.append(int(data[y1][x1:x2]))
    return numbers 

def part_1(data):
    number_pattern = re.compile(r'(\d+)')
    engine_parts = []
    for i, line in enumerate(data):
        num_matches = number_pattern.finditer(line)
        for num_match in num_matches:
            x1, x2 = num_match.span()
            if not has_adjacent_symbol(data, r"[^a-zA-Z0-9.]", (x1, x2, i)):
                continue
            engine_parts.append(int(num_match.group(0)))
    return engine_parts

def part_2(data):
    gear_pattern = re.compile(r'\*')
    gear_ratios = []
    for i, line in enumerate(data):
        gear_matches = gear_pattern.finditer(line)
        for gear_match in gear_matches:
            x1, x2 = gear_match.span()
            numbers = has_adjacent_symbol(data, r"(\d+)", (x1, x2, i))
            if len(numbers) != 2:
                continue
            entire_numbers = find_entire_numbers(data, x1, i)
            gear_ratios.append(entire_numbers[0]*entire_numbers[1])
    return gear_ratios

def main():
    input = 'input.txt'
    data = parse(input)
    print("Part 1: ", sum(part_1(data))) # 557705
    print("Part 2: ", sum(part_2(data))) # 

if __name__ == '__main__':
    main()
