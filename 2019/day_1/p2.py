import sys

def calc_fuel(mass):
    if mass//3-2 < 0:
        return 0
    new_mass = mass//3-2
    return new_mass + calc_fuel(new_mass)

def part_2():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    return sum([calc_fuel(int(num)) for num in open(infile).read().strip().split('\n')])

if __name__ == "__main__":
    print("Part 2: ", part_2())