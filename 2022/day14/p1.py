from aocd import get_data
import numpy as np

def gen_ranges(stone_rngs):
	stones = []
	for stone_rng in stone_rngs:
		points = []
		for stone in stone_rng.split("->"):
			points.append(tuple(int(i) for i in stone.split(",")))
		for i in range(len(points)-1):
			x1, y1 = points[i]
			x2, y2 = points[i+1]
			if x1 == x2:
				# Horizontal line
				start_y = min(y1, y2)
				end_y = max(y1, y2)
				for y in range(start_y, end_y + 1):
					stones.append((x1, y))
			elif y1 == y2:
				# Vertical line
				start_x = min(x1, x2)
				end_x = max(x1, x2)
				for x in range(start_x, end_x + 1):
					stones.append((x, y1))
	return stones


def create_world(stone_rngs):
	stones = gen_ranges(stone_rngs)
	cave = np.chararray((max(stones, key=lambda x: x[1])[1]+1, max(stones, key=lambda x: x[0])[0]+1), itemsize=1, unicode=True)
	cave[:] = "."
	for stone in stones:
		cave[stone[1], stone[0]] = "#"
	return cave

def simulate(cave):
	count = 0
	x, y = 500, 0
	while x == 500 and y == 0:
		for delta_y in range(1, len(cave)):
			if cave[y + delta_y][x] in ['#', 'o']:
				if cave[y + delta_y][x - 1] not in ['#', 'o']:
					x -= 1
				elif cave[y + delta_y][x + 1] not in ['#', 'o']:
					x += 1
				else:
					count += 1
					cave[y + delta_y-1][x] = "o"
					x, y = 500, 0
					break
	return count
if __name__ == '__main__':
	stone_rngs = get_data(day=14, year=2022).splitlines()
	cave = create_world(stone_rngs)
	print("Part 1: ", simulate(cave))