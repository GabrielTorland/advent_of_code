import sys

def intersections(rucksacks):
    r_1, r_2, r_3 = set(rucksacks[0]), set(rucksacks[1]), set(rucksacks[2])
    return r_1 & r_2 & r_3 

if __name__ == "__main__":
    rucksacks = open(sys.argv[1] if len(sys.argv) > 1 else "input.in").read().split("\n")
    print(sum([sum([ord(i) - 96 if ord(i) > 96 else ord(i) - 38 for i in intersections(rucksacks[i:i+3])]) for i in range(0, len(rucksacks), 3)]))