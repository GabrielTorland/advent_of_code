def parse(input_file="input.txt"):
    return [[plant for plant in line] for line in open(input_file).read().splitlines()]


def get_plant_field(i, j, grid, visited):
    """Finds all the plants in the same plant field as the plant at (i, j)"""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbors = [(i, j)]
    for di, dj in directions:
        if 0 <= (i + di) < len(grid) and 0 <= (j + dj) < len(grid[0]) and (i+di, j+dj) not in visited and grid[i+di][j+dj] == grid[i][j]:
            visited.add((i+di, j+dj))
            neighbors += get_plant_field(i+di, j+dj, grid, visited)
    return neighbors

def calculate_circumference(plant_field):
    directions = [(0, 1, "right"), (0, -1, "left"), (1, 0, "down"), (-1, 0, "up")]
    sides = set()
    for i, j in plant_field:
        for di, dj, direction in directions:
            if (i+di, j+dj) not in plant_field:
                sides.add((i, j, direction))
    return len(sides)

def calculate_circumference_v2(plant_field):
    directions = [(0, 1, "right"), (0, -1, "left"), (1, 0, "down"), (-1, 0, "up")]
    sides = set()
    for i, j in plant_field:
        for di, dj, direction in directions:
            if (i+di, j+dj) not in plant_field:
                sides.add((i, j, direction))
    longer_sides = set()
    for i, j, direction in sides:
        horizontal_side = [(i, j)]
        vertical_side = [(i, j)]
        if direction == "up" or direction == "down":
            # right
            k = 0
            while (i, j + k + 1, direction) in sides:
                horizontal_side.append((i, j+k+1))
                k+=1
            # left
            k = 0
            while (i, j - k - 1, direction) in sides:
                horizontal_side.insert(0, (i, j-k-1))
                k+=1
        else:
            # down
            k = 0
            while (i + k + 1, j, direction) in sides:
                vertical_side.append((i+k+1, j))
                k+=1
            # up
            k = 0
            while (i - k - 1, j, direction) in sides:
                vertical_side.insert(0, (i-k-1, j))
                k+=1

        if len(horizontal_side) > 1:
            longer_sides.add((horizontal_side[0], horizontal_side[-1], direction))
        if len(vertical_side) > 1:
            longer_sides.add((vertical_side[0], vertical_side[-1], direction))

    for ((i, j), (k, l), direction) in longer_sides:
        if direction in ["up", "down"]:
            for m in range(j, l+1):
                if (i, m, direction) in sides:
                    sides.remove((i, m, direction))
        else:
            for m in range(i, k+1):
                if (m, j, direction) in sides:
                    sides.remove((m, j, direction))


    return len(sides)+len(longer_sides)

def calculate_cost(plant_field, circumference_function=calculate_circumference):
    circumference = circumference_function(plant_field)
    return circumference * len(plant_field)

def p1(grid):
    plant_fields = []
    visited = set()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in visited:
                visited.add((i, j))
                plant_fields.append(get_plant_field(i, j, grid, visited))
    return sum([calculate_cost(plant_field) for plant_field in plant_fields])

def p2(grid):
    plant_fields = []
    visited = set()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in visited:
                visited.add((i, j))
                plant_fields.append(get_plant_field(i, j, grid, visited))
    return sum([calculate_cost(plant_field, circumference_function=calculate_circumference_v2) for plant_field in plant_fields])



if __name__ == "__main__":
    grid = parse()
    print("Part 1:", p1(grid))
    print("Part 2:", p2(grid))