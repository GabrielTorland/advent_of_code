from aocd import get_data
import re


def parse(raw):
	scanners = []
	beacons = []
	for line in raw:
		l1, l2 = line.split(': ')
		scanners.append(tuple(int(num) for num in re.search(r'x=(-?\d+), y=(-?\d+)', l1).groups()))	
		beacons.append(tuple(int(num) for num in re.search(r'x=(-?\d+), y=(-?\d+)', l2).groups()))
	return scanners, beacons 

class Range:
	def __init__(self, start, end) -> None:
		self.start = start
		self.end = end
		self.size = end - start + 1

	def __repr__(self):
		return f"Range({self.start}, {self.end})"

def merge(row_ranges):
	row_ranges.sort(key=lambda r: r.start)
	new_row_ranges = [row_ranges.pop(0)]
	i = 0 
	for rng in row_ranges:
		if new_row_ranges[i].end < rng.start-1:
			new_row_ranges.append(rng)
			i += 1
		elif new_row_ranges[i].end < rng.end: 
			new_row_ranges[i] = Range(new_row_ranges[i].start, rng.end)
	return new_row_ranges	
			
def calc_euclidean_distance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def update_ranges(ranges, scanner, beacon, n):
	euc_dist = calc_euclidean_distance(scanner, beacon)
	
	top = (scanner[1] - euc_dist) if (scanner[1] - euc_dist) >= 0 else 0
	d = euc_dist - abs(top - scanner[1])
	for i in range(top, scanner[1]+1):
		ranges[i].append(Range(scanner[0] - d if (scanner[0] - d) >= 0 else 0, scanner[0] + d if (scanner[0] + d) <= n else n))
		ranges[i] = merge(ranges[i])
		d += 1

	d = euc_dist - 1	
	for i in range(scanner[1] + 1, (scanner[1] + euc_dist+1) if (scanner[1] + euc_dist+1) <= n+1 else n+1):
		ranges[i].append(Range(scanner[0] - d if (scanner[0] - d) >= 0 else 0, scanner[0] + d if (scanner[0] + d) <= n else n))
		ranges[i] = merge(ranges[i])
		d -= 1

def find_free_entry(ranges, n):
	for y, row_ranges in enumerate(ranges):
		if len(row_ranges) > 1:
			return (row_ranges[0].end + 1, y)
		if row_ranges[0].size < n + 1:
			return (n if row_ranges[0].start == 0 else 0, y) 

if __name__ == '__main__':
	raw = get_data(day=15, year=2022).splitlines()
	scanners, beacons = parse(raw)
	n = 4000000
	ranges = [[] for _ in range(n+1)]
	for scanner, beacon in zip(scanners, beacons):
		update_ranges(ranges, scanner, beacon, n)
	x, y = find_free_entry(ranges, n)
	print("Part 2: ", x*n + y)
