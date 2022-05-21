import sys, math
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
        # Sea cucumbers moving east at index w = 0 and south at index h = 1
        for w in range(2):    
            moved_on = set()
            for i, row in enumerate(cu_map):
                for j, elem in enumerate(row):
                    if (i,j) in moved_on: continue
                    if w == 0:
                        y = j+1 if j+1 <= len(row)-1 else 0
                        if elem == '>' and cu_map[i][y] == '.' and (i,y) not in moved_on:
                            new_cu_map[i][j] = '.'
                            new_cu_map[i][y] = elem
                            moved_on = moved_on.union({(i,j), (i,y)})
                            moved += 1
                        else:
                            new_cu_map[i][j] = elem
                    else:
                        x = i+1 if i+1 <= len(cu_map)-1 else 0
                        if new_cu_map[i][j] == 'v' and new_cu_map[x][j] == '.' and (x,j) not in moved_on:
                            new_cu_map[i][j] = '.'
                            new_cu_map[x][j] = 'v'
                            moved_on = moved_on.union({(x, j), (i, j)})
                            moved += 1
        steps += 1
        cu_map = new_cu_map
    return steps
    

if __name__ == '__main__':
    cu_map = parse()
    print("Part 1: ", find_steady_state(cu_map))