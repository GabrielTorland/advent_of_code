import sys
from functools import lru_cache
from collections import defaultdict

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    with open(infile, 'r') as f:
        return sorted([0]+[int(line) for line in f.read().splitlines()])

def possible_jumps(joltages):
    possible_jumps = defaultdict(lambda: list())
    for i, jol_1 in enumerate(joltages):
        if i > len(joltages) - 1:
            break
        for jol_2 in joltages[i+1:]:
                if jol_2-jol_1 in [1, 2, 3]:
                    possible_jumps[jol_1].append(jol_2)
                else:
                    break
    return possible_jumps

@lru_cache()
def calculate_combinations(joltage):
    global possible_jumps
    combs = 0
    if joltage == destination:
        return 1
    for next_joltage in possible_jumps[joltage]:
        combs += calculate_combinations(next_joltage)
    return combs

joltages = parse()
destination = max(joltages)
possible_jumps = possible_jumps(joltages)
print("Possible combinations:", calculate_combinations(0))
