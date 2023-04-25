import sys

def part_1():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    return sum([int(num)//3-2 for num in open(infile).read().strip().split('\n')])

if __name__ == "__main__":
    print("Part 1: ", part_1())