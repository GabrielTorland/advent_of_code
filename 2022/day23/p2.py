from collections import defaultdict 
from aocd import get_data

class Instructions:
	def move(self, grid, i, j, k):
		if k % 4 == 0:
			return self.move_north(grid, i, j, 4)
		elif k % 4 == 1:
			return self.move_south(grid, i, j, 4)
		elif k % 4 == 2:
			return self.move_west(grid, i, j, 4)	
		else:
			return self.move_east(grid, i, j, 4)

	def move_north(self, grid, i, j, n):
		if n == 0: return i, j
		for pos in [(i-1, j), (i-1, j-1), (i-1, j+1)]:
			if pos in grid: return self.move_south(grid, i, j, n-1)
		return i-1, j
	def move_south(self, grid, i, j, n):
		if n == 0: return i, j	
		for pos in [(i+1, j), (i+1, j+1), (i+1, j-1)]:
			if pos in grid: return self.move_west(grid, i, j, n-1)
		return i+1, j
	def move_west(self, grid, i, j, n):
		if n == 0: return i, j
		for pos in [(i, j-1), (i-1, j-1), (i+1, j-1)]:
			if pos in grid: return self.move_east(grid, i, j, n-1)
		return i, j-1
	def move_east(self, grid, i, j, n):
		if n == 0: return i, j
		for pos in [(i, j+1), (i+1, j+1), (i-1, j+1)]:
			if pos in grid: return self.move_north(grid, i, j, n-1)
		return i, j+1

def parse(raw):
	grid = {}
	for i, line in enumerate(raw.splitlines()):
		for j, entry in enumerate(line):
			if entry == '#':
				grid[(i, j)] = '#'
	return grid

def moving(grid, i, j):
	return (i, j-1) in grid or (i+1, j-1) in grid or (i-1, j-1) in grid or (i, j+1) in grid or (i+1, j+1) in grid or (i-1, j+1) in grid or (i-1, j) in grid or (i+1, j) in grid

def simulate(grid):
	instructions = Instructions()
	moved = True
	k = 0 
	while moved:
		destinations = defaultdict(set)
		moved = False
		for (i, j), _ in grid.items():
			if not moving(grid, i, j): 
				destinations[(i, j)].add((i, j))
				continue
			destinations[instructions.move(grid, i, j, k)].add((i, j))
			moved = True
		grid = {}
		for (i, j), source in destinations.items():
			if len(source) == 1:
				grid[(i, j)] = '#'
			else:
				for pos in source:
					grid[pos] = '#'
		k += 1
	return grid, k

def print_state(grid):
	x_range, y_range = min_square(grid)
	for i in y_range:
		for j in x_range:
			print(grid.get((i, j), '.'), end='')
		print()
	print()	
		
def min_square(grid):
	return range(min(grid.keys(), key=lambda x: x[1])[1], max(grid.keys(), key=lambda x: x[1])[1] + 1), range(min(grid.keys(), key=lambda x: x[0])[0], max(grid.keys(), key=lambda x: x[0])[0] + 1)

def empty_squares(grid, x_range, y_range):
	return sum([1 for i in y_range for j in x_range if (i, j) not in grid.keys()])

if __name__ == '__main__':
	raw = get_data(day=23, year=2022)
	grid = parse(raw)
	grid, k = simulate(grid)
	print("Part 2: ", k) # 965