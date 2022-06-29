import sys
import numpy as np

def parse():
    """
    Parse the input file and return a list of lists of integers.
    """
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    with open(infile) as f:
        # Convert list to numpy array
        input = np.array([int(elem) for elem in f.read().strip().split(',')])
        input[1] = 12
        input[2] = 2
        return input

def part_1(input):
    i = 0   
    while input[i] != 99:
        if input[i] == 1:
            input[input[i+3]] = input[input[i+1]] + input[input[i+2]]
        elif input[i] == 2:
            input[input[i+3]] = input[input[i+1]]*input[input[i+2]]
        else:
            print("Error!")
        i += 4
    return input[0]

if __name__ == "__main__":
    print("Part 1: ", part_1(parse()))