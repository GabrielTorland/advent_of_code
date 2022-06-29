

import sys
import numpy as np

def parse():
    """
    Parse the input file and return a list of lists of integers.
    """
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    with open(infile) as f:
        # Convert list to numpy array
        return np.array([int(elem) for elem in f.read().strip().split(',')])

def part_2(org_input):
    a = 0
    b = 0
    while True:
        input = org_input.copy()
        input[1] = a
        input[2] = b
        i = 0
        while input[i] != 99:
            if input[i] == 1:
                input[input[i+3]] = input[input[i+1]] + input[input[i+2]]
            elif input[i] == 2:
                input[input[i+3]] = input[input[i+1]]*input[input[i+2]]
            else:
                print("Error!")
            i += 4
        if input[0] == 19690720:
            return 100*a + b
        if input[0] != 1:
            print()
        if b >= len(org_input)-2:
            if b == 1:
                print("Error!")
                return None
            a += 1
            b = 1
        else:
            b += 1


if __name__ == "__main__":
    print("Part 2: ", part_2(parse()))