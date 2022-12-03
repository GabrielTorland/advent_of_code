import sys

def intersections(rucksack):
    n = len(rucksack)
    c_1, c_2 = set(rucksack[:n//2]), set(rucksack[n//2:])
    i = c_1.intersection(c_2)
    return i

if __name__ == "__main__":
    rucksacks = open(sys.argv[1] if len(sys.argv) > 1 else "input.in").read().split("\n")
    print(sum([sum([ord(i) - 96 if ord(i) > 96 else ord(i) - 38 for i in intersections(rucksack)]) for rucksack in rucksacks]))
    

