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

def calc_manhattan_distance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def gen_points_in_row(scanners, beacons, row):
	points = set()
	for scanner, beacon in zip(scanners, beacons):
		euc_d = calc_manhattan_distance(scanner, beacon)
		if euc_d < abs(scanner[1] - row): continue
		for euc in range(abs(scanner[1] - row), euc_d + 1):
			for x, y in set([(euc - abs(scanner[1] - row) + scanner[0], row), (abs(scanner[1] - row) - euc + scanner[0], row)]):
				if (x, y) in beacons: continue
				points.add((x, y))
	return points

if __name__ == '__main__':
	raw = get_data(day=15, year=2022).splitlines()
	scanners, beacons = parse(raw)
	n = 2000000 
	print("Part 1: ", len(gen_points_in_row(scanners, beacons, n)))