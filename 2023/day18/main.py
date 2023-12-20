import re
import numpy as np
from collections import defaultdict

def parse_input(input_path="input.txt"):
	with open(input_path, "r") as f:
		for line in f.readlines():
			line = line.strip()
			direction, steps, color =  re.search(r"([RLUD]) (\d+) \((.*)\)", line).groups()
			yield direction, int(steps), color

def get_volume_in_lagoon(edges_color):
	min_x = min(edges_color, key=lambda e: e[0])[0]
	max_x = max(edges_color, key=lambda e: e[0])[0]
	min_y = min(edges_color, key=lambda e: e[1])[1]
	max_y = max(edges_color, key=lambda e: e[1])[1]
	volume_lagoon = 0
	in_polygon = set()
	edge_cases = set() 
	lagoon_map = np.full((max_x-min_x+1, max_y-min_y+1), '.')
	for i in range(min_x+1, max_x):
		for j in range(min_y+1, max_y):
			if (i, j) in edges_color: continue
			under = "".join('#' if (k, j) in edges_color else '.' for k in range(i, max_x+1))
			over = "".join('#' if (k, j) in edges_color else '.' for k in range(i, min_x-1, -1))
			right = "".join('#' if (i, k) in edges_color else '.' for k in range(j, max_y+1))
			left = "".join('#' if (i, k) in edges_color else '.' for k in range(j, min_y-1, -1))
			edge_case = True 
			for line in (under, over, right, left):
				if re.search(r"##+", line): continue
				if len(re.findall(r'#', line)) % 2 == 1:
					volume_lagoon += 1
					lagoon_map[i-min_x, j-min_y] = '#'
					in_polygon.add((i, j))
				edge_case = False
				break
			if edge_case:
				edge_cases.add((i, j))    
	
	while len(edge_cases):
		previous_len = len(edge_cases)
		resolved = set()
		for (x, y) in edge_cases:
			for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
				if (x+dx, y+dy) in in_polygon:
					volume_lagoon += 1
					lagoon_map[x-min_x, y-min_y] = '#'
					in_polygon.add((x, y))
					resolved.add((x, y))
					break
		edge_cases -= resolved
		if previous_len == len(edge_cases):
			break
		print("Hi mom!")
	np.savetxt("lagoon_map.txt", lagoon_map, fmt="%s")

	return volume_lagoon+len(edges_color)

def part_1_slow(edges_gen):
	edges_color = {}
	x, y = 0, 0
	dir_to_coord = {
		"R": (0, 1),
		"L": (0, -1),
		"U": (-1, 0),
		"D": (1, 0)
	} 
	for direction, steps, color in edges_gen:
		for i in range(steps):
			dx, dy = dir_to_coord[direction]
			x += dx
			y += dy
			edges_color[(x, y)] = color
	return get_volume_in_lagoon(edges_color)

def shoe_lace_algorithm(vertices):
    n = len(vertices)
    return abs(sum(vertices[i][0] * vertices[(i + 1) % n][1] - vertices[(i + 1) % n][0] * vertices[i][1] for i in range(n))) // 2

def picks_theorem(A, b):
	return A - b/2 + 1
	
def part_1_fast(edges_gen):
	x, y = 0, 0
	dir_to_coord = {
		"R": (0, 1),
		"L": (0, -1),
		"U": (-1, 0),
		"D": (1, 0)
	} 
	vertices = []
	b = 0
	for direction, steps, color in edges_gen:
		dx, dy = dir_to_coord[direction]
		x += dx*steps
		y += dy*steps
		vertices.append((x, y))
		b += steps
	A = shoe_lace_algorithm(vertices)
	return picks_theorem(A, b) + b

def part_2(edges):
	dir_to_coord = {
		0: (0, 1),
		2: (0, -1),
		3: (-1, 0),
		1: (1, 0)
	}
	edges = [(dir_to_coord[int(color[-1])], int(color[1:-1], 16)) for direction, steps, color in edges if color[-1]]
	x, y = 0, 0 
	vertices = [] 
	b = 0
	for direction, steps in edges:
		dx, dy = direction
		x += dx*steps
		y += dy*steps
		vertices.append((x, y))
		b += steps

	A = shoe_lace_algorithm(vertices)
	return picks_theorem(A, b) + b

def main():
	edges_gen = parse_input()
	print("Part 1: ", part_1_fast(edges_gen))
	edges = list(parse_input())
	print("Part 2: ", part_2(edges))


if __name__ == "__main__":
	main()