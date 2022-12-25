from aocd import get_data
from collections import defaultdict


if __name__ == "__main__":
	lava_droplets = [tuple(int(elem) for elem in coord.split(',')) for coord in get_data(day=18, year=2022).splitlines()]
	world = defaultdict(int)
	sides = 0
	for x, y, z in lava_droplets:
		world[(x, y, z)] = 1
		sides += -1 if world[(x+1, y, z)] else 1
		sides += -1 if world[(x-1, y, z)] else 1
		sides += -1 if world[(x, y+1, z)] else 1
		sides += -1 if world[(x, y-1, z)] else 1
		sides += -1 if world[(x, y, z+1)] else 1
		sides += -1 if world[(x, y, z-1)] else 1
	print("Part 1: ", sides)
		



		