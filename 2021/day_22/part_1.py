import sys
from collections import defaultdict, Counter


def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    cubes = set()
    with open(infile, 'r') as f:
        for line in f.readlines():
            data = line.strip().split(' ')
            new_cubes = set()
            tmp_cubes = [list(range(int(rng[2:].split("..")[0]), int(rng[2:].split("..")[1])+1)) for rng in data[1].split(',')]
            new_cubes = {(int(tmp_cubes[0][i]), int(tmp_cubes[1][i]), int(tmp_cubes[2][i])) for i in range(len(tmp_cubes[0]))}
            if data[0] == 'on':
                cubes = cubes.union(new_cubes)
            else:
                cubes = cubes-new_cubes
    return cubes
                
def count_cubes(cubes):
    in_range = set()
    for x, y, z in cubes:
        if -50 <= x <= 50 and -50 <= y <= 50 and -50 <= z <= 50:
            in_range.add((x, y, z))
    return len(in_range)

if __name__ == '__main__':
    cubes = parse()
    print("Part 1:", count_cubes(cubes))

