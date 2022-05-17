import sys, re
from itertools import product

GROUPS = 14

# I split the operations into groups, where each group start with inp.
# There are 7 groups that add a value to z, and 7 that subract from z.
# In the 7 groups that subtract from z we can detemine w. If there is no valid w we simply try next sequence.
# type 1: z = 26z+w+c2, c2 different for type 1 groups.
# type 2: z = w+11+26*z//26 or z = z//26. But z has to decrease all 7 rounds to reach 0, therefore z = z//26.
# To figure out w in a type 2 group we need to check if (z%26)+c1 is a valid w.

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    return [instruction.split(' ') for instruction in open(infile).read().split('\n')]

def find_model_number(instructions, input_space):
    c1 = list()
    c2 = list()
    group = 0
    for i in range(GROUPS): # 14 groups
        c1.append(int(instructions[group+5][2]))
        c2.append(int(instructions[group+15][2]))
        group += 18
    
    for input in input_space:
        numbers = {}
        z = 0
        p = 0
        failed = False
        for i in range(GROUPS):
            assert z >= 0
            if c1[i] < 0:
                # Has to be a valid w for this sequence to work. 
                if (z%26)+c1[i] > 9 or (z%26)+c1[i] <= 0:
                    failed = True
                    break
                # Store w to reassemble the sequence later.
                numbers[i] = (z%26)+c1[i]
                z //= 26
            else:
                z = 26*z+input[p]+c2[i]
                p += 1
        if z == 0 and not failed:
            tmp = list(input)[::-1]
            return [tmp.pop() if i not in numbers.keys() else numbers[i] for i in range(GROUPS)]


if __name__ == '__main__':
    instructions = parse()
    print("part 1: ", "".join(str(digit) for digit in find_model_number(instructions, input_space = product(range(9, 0, -1), repeat=GROUPS//2))))
    print("part 2: ", "".join(str(digit) for digit in find_model_number(instructions, input_space = product(range(1,10), repeat=GROUPS//2))))