from itertools import permutations

# Add all avtive cells to a set called active
def parse():
    with open('input.txt', 'r') as f:
        cells = set()
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    cells.add((x, y, 0))
    return cells

 
# The new era for the next generation
# Active cells cant be generated outside this era in the next generation. 
def bounds(cells):
    res = []
    for i in range(3):
        res.append(min(cells, key=lambda x: x[i])[i] - 1)
        res.append(max(cells, key=lambda x: x[i])[i] + 2)
    return res

def get_active_count(x, y, z, cells):
    res = 0
    for dx in range(-1,2):
        for dy in range(-1,2):
            for dz in range(-1,2):
                if not (dx == dy == dz == 0) and  ((x+dx, y+dy, z+dz) in cells):
                    res += 1
    return res

def simulate(cells):
    current_bounds = bounds(cells)
    next_cells = set()
    for x in range(current_bounds[0], current_bounds[1]):
        for y in range(current_bounds[2], current_bounds[3]):
            for z in range(current_bounds[4], current_bounds[5]):
                if (x, y, z) in cells:
                    if get_active_count(x, y, z, cells) in [2, 3]:
                        next_cells.add((x, y, z))
                else:
                    if get_active_count(x, y, z, cells) == 3:
                        next_cells.add((x, y, z))
    return next_cells

cells = parse()
for generation in range(1, 6+1):
    cells = simulate(cells)
print(len(cells))
