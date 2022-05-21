import sys, math, copy
import numpy as np

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    return np.asanyarray([[elem for elem in row] for row in open(infile).read().split('\n')])

def find_steady_state(cu_map):
    moved = math.inf
    steps = 0
    while moved > 0:
        new_cu_map = np.empty((len(cu_map), len(cu_map[0])), dtype=str)
        moved = 0
        # Sea cucumbers moving east
        for i, row in enumerate(cu_map):
            skip_next = False
            for j, elem in enumerate(row):
                if skip_next:
                    skip_next = False
                    continue
                y = j+1 if j+1 <= len(row)-1 else 0
                if elem == '>' and cu_map[i][y] == '.':
                    new_cu_map[i][j] = '.'
                    new_cu_map[i][y] = elem
                    skip_next = True
                    moved += 1
                else:
                    new_cu_map[i][j] = elem
        
        # Sea cucumbers moving south
        cu_map = copy.copy(new_cu_map)
        for j in range(len(new_cu_map[0])):
            skip_next = False
            for i in range(len(new_cu_map)):
                if skip_next:
                    skip_next = False
                    continue
                x = i+1 if i+1 <= len(cu_map)-1 else 0
                if cu_map[i][j] == 'v' and cu_map[x][j] == '.':
                    new_cu_map[i][j] = '.'
                    new_cu_map[x][j] = 'v'
                    skip_next = True
                    moved += 1
                else:
                    new_cu_map[i][j] = cu_map[i][j]
        steps += 1
        cu_map = new_cu_map
    return steps
    



if __name__ == '__main__':
    cu_map = parse()
    print("Part 1: ", find_steady_state(cu_map))