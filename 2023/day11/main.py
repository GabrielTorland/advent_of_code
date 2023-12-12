from itertools import combinations
import heapq
import numpy as np

def parse_input(input_path):
	return np.array([np.array([char for char in line.strip()]) for line in open(input_path).readlines()])

def expand_universe(universe_map):
	"""Expands universe by duplicating rows and columns that doesn't contain any galaxy."""
	new_universe_map = []

	# Update columns
	for i in range(universe_map.shape[1]):
		column = universe_map[:, i]
		for _ in range(1 if '#' in column else 2):
			for j, val in enumerate(column):
				if j >= len(new_universe_map):
					new_universe_map.append([])
				new_universe_map[j].append(val)
	# Update rows
	nr_inserted_rows = 0 
	for i, row in enumerate(universe_map):
		if '#' in row: continue
		new_universe_map.insert(i+nr_inserted_rows, new_universe_map[i+nr_inserted_rows])
		nr_inserted_rows += 1
	
	return np.array([np.array(row) for row in new_universe_map])


def dijkstra(universe_map, start):
	# Initialize distances with infinity, except for the start node
	distances = {(i, j): float('inf') for i in range(len(universe_map)) for j in range(len(universe_map[0]))}
	distances[start] = 0

	# Priority queue to hold nodes to visit
	queue = [(0, start)]

	while queue:
		# Get the node with the smallest distance
		current_distance, (i, j) = heapq.heappop(queue)

		# If this distance is already larger than the known smallest, skip
		if current_distance > distances[(i, j)]:
			continue

		# Explore neighbors
		for (k, l) in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
			if k < 0 or k >= len(universe_map) or l < 0 or l >= len(universe_map[0]):
				continue

			distance = current_distance + 1 

			# If a shorter path is found
			if distance < distances[(k, l)]:
				distances[(k, l)] = distance
				heapq.heappush(queue, (distance, (k, l)))

	return distances

def extra_distance_after_expansion(universe_map, galaxies, expansion_rate):
	"""Calculates the extra distance between two galaxies after the universe has expanded."""
	extra_distance = 0
	for i in range(min(galaxies, key=lambda x: x[0])[0], max(galaxies, key=lambda x: x[0])[0]):
		if '#' in universe_map[i]: continue
		extra_distance += expansion_rate - 1 
	for j in range(min(galaxies, key=lambda x: x[1])[1], max(galaxies, key=lambda x: x[1])[1]):
		if '#' in universe_map[:, j]: continue
		extra_distance += expansion_rate - 1
	return extra_distance


def part_2(universe_map):
	"""Calculates the sum of the shortest paths between all pairs of galaxies, but with a more effective method of handling expansion."""
	shortest_paths = {}
	for i, row in enumerate(universe_map):
		for j in np.where(row == '#')[0]:
			shortest_paths[(i, j)] = dijkstra(universe_map, (i, j))
	sum_shortest_paths = 0
	for (i, j), (k, l) in combinations(shortest_paths.keys(), 2):
		sum_shortest_paths += shortest_paths[(k, l)][(i, j)] + extra_distance_after_expansion(universe_map, [(i, j), (k, l)], 1000000)  
	return sum_shortest_paths

def part_1(universe_map):
	"""Calculates the sum of the shortest paths between all pairs of galaxies."""
	universe_map = expand_universe(universe_map)
	shortest_paths = {}
	for i, row in enumerate(universe_map):
		for j in np.where(row == '#')[0]:
			shortest_paths[(i, j)] = dijkstra(universe_map, (i, j))
	sum_shortest_paths = 0
	for (i, j), (k, l) in combinations(shortest_paths.keys(), 2):
		sum_shortest_paths += shortest_paths[(k, l)][(i, j)] 
	return sum_shortest_paths


def main():
	universe_map = parse_input('input.txt')
	print("Part 1: ", part_1(universe_map)) # 9550717
	print("Part 2: ", part_2(universe_map)) # 648458253817

if __name__ == '__main__':
	main()