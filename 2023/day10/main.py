import re, sys
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import heapq
import numpy as np

sys.setrecursionlimit(100000)

def parse_input(input_path):
	def construct_network(raw_rows, i, j, network, visited=set()):
		visited.add((i, j))
		if raw_rows[i][j] in ['S', '|', 'J', 'L'] and (i-1) >= 0 and raw_rows[i-1][j] in ['|', '7', 'F', 'S']:
			network[(i, j)].append((i-1, j))
			if not (i-1, j) in visited: construct_network(raw_rows, i-1, j, network, visited)
		if raw_rows[i][j] in ['S', '|', 'F', '7'] and (i+1) < len(raw_rows) and raw_rows[i+1][j] in ['|', 'L', 'J', 'S']:
			network[(i, j)].append((i+1, j))
			if not (i+1, j) in visited: construct_network(raw_rows, i+1, j, network, visited)
		if raw_rows[i][j] in ['S', '-', 'J', '7'] and (j-1) >= 0 and raw_rows[i][j-1] in ['-', 'L', 'F', 'S']:
			network[(i, j)].append((i, j-1))
			if not (i, j-1) in visited: construct_network(raw_rows, i, j-1, network, visited)
		if raw_rows[i][j] in ['S', '-', 'F', 'L'] and (j+1) < len(raw_rows[i]) and raw_rows[i][j+1] in ['-', '7', 'J', 'S']:
			network[(i, j)].append((i, j+1))
			if not (i, j+1) in visited: construct_network(raw_rows, i, j+1, network, visited)
	raw_rows = open(input_path, 'r').readlines()
	network = defaultdict(list)
	for i, row in enumerate(raw_rows):
		start = re.search(r'S', row.strip())
		if not start: continue
		j = start.start()
		start_position = (i, j)
		construct_network(raw_rows, i, j, network)
	return np.array([np.array([val for val in row.strip()]) for row in raw_rows]), network, start_position

def visualize_network(network):
	G = nx.Graph()

	for key, values in network.items():
		for value in values:
			G.add_edge(key, value)

	plt.figure(figsize=(22, 22))

	pos = nx.shell_layout(G)  # using shell layout
	nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=200, width=0.5, font_size=8)
	plt.show()

def dijkstra(graph, start):
	# Initialize distances with infinity, except for the start node
	distances = {node: float('inf') for node in graph}
	distances[start] = 0

	# Priority queue to hold nodes to visit
	queue = [(0, start)]

	while queue:
		# Get the node with the smallest distance
		current_distance, current_node = heapq.heappop(queue)

		# If this distance is already larger than the known smallest, skip
		if current_distance > distances[current_node]:
			continue

		# Explore neighbors
		for neighbor in graph[current_node]:
			distance = current_distance + 1 

			# If a shorter path is found
			if distance < distances[neighbor]:
				distances[neighbor] = distance
				heapq.heappush(queue, (distance, neighbor))

	return distances

def part_1(network, start_position):
	distances = dijkstra(network, start_position)
	return max(distances.values()) 

def fill_map(map, network, i, j, visited=set()):
	# Fill upwards
	above = (i - 1) >= 0
	not_visited = (i-1, j) not in visited
	not_in_network = (i-1, j) not in network
	if above and not_visited and not_in_network:
		visited.add((i-1, j))
		visited = fill_map(map, network, i-1, j, visited)
	
	# Fill downwards
	below = (i + 1) < len(map)
	not_visited = (i+1, j) not in visited
	not_in_network = (i+1, j) not in network
	if below and not_visited and not_in_network:
		visited.add((i+1, j))
		visited = fill_map(map, network, i+1, j, visited)

	# Fill leftwards
	left = (j - 1) >= 0
	not_visited = (i, j-1) not in visited 
	not_in_network = (i, j-1) not in network
	if left and not_visited and not_in_network:
		visited.add((i, j-1))
		visited = fill_map(map, network, i, j-1, visited)

	# Fill rightwards
	right = (j + 1) < len(map[i])
	not_visited = (i, j+1) not in visited 
	not_in_network = (i, j+1) not in network
	if right and not_visited and not_in_network:
		visited.add((i, j+1))
		visited = fill_map(map, network, i, j+1, visited)

	return visited
	
def is_not_enclosed(map, cluster):
	if 0 in [i for i, j in cluster]: return True 
	if len(map) - 1 in [i for i, j in cluster]: return True
	if 0 in [j for i, j in cluster]: return True
	if len(map[0]) - 1 in [j for i, j in cluster]: return True
	return False

def is_valid_position(map, pos):
	(i, j), (k, l) = pos
	if i < 0 or i >= len(map): return False
	if j < 0 or j >= len(map[i]): return False
	if k < 0 or k >= len(map): return False
	if l < 0 or l >= len(map[k]): return False
	return True


def connect_to_other_cluster(map, network, i, j, k, l, direction, visited):
	# Check if current positions are part of the network
	if (i, j) not in network and (i, j) not in visited:
		return set([(i, j)]) 
	if (k, l) not in network and (k, l) not in visited:
		return set([(k, l)]) 

	# Define valid symbols for different directionections
	valid_symbols = {
 		'up': {0: [set(['|', 'J', '7']), set(['|', 'F', 'L'])], 1: [set(['7']), set(['-', 'L', 'J'])], 2: [set(['F']), set(['-', 'J', 'L'])]},
		'down': {0: [set(['|', 'J', '7']), set(['|', 'F', 'L'])], 1: [set(['-', '7', 'F']), set(['J' ])], 2: [set(['-', '7', 'F']), set(['L'])]},
		'left': {0: [set(['-', 'F', '7']), set(['-', 'J', 'L'])], 1: [set(['|', '7', 'J']), set(['F'])], 2: [set(['|', '7', 'J']), set(['L'])]},
		'right': {0: [set(['-', '7', 'F']), set(['-', 'J', 'L'])], 1: [set(['7']), set(['|', 'L', 'F'])], 2: [set(['J']), set(['|', 'F', 'L'])]},
		'universal': set(['.', 'I'])
	}

	# Calculate next positions based on directionection
	next_positions = {
		'up': [((i - 1, j), (k - 1, l)), ((k, l-1), (i-1, j)), ((i, j+1), (k-1, l))], # up up, up left, up right
		'down': [((i + 1, j), (k + 1, l)), ((i+1, j), (k, l-1)), ((k+1, l), (i, j+1))], # down down, down left, down right
		'left': [((i, j - 1), (k, l - 1)), ((i, j-1), (k+1, l)), ((k, l-1), (i-1, j))], # left left, left down, left up
		'right': [((i, j + 1), (k, l + 1)), ((k+1, l), (i, j+1)), ((i-1, j), (k, l+1))] # right right, right down, right up
	}

	next_direction = {
		'up': ['up', 'left', 'right'],
		'down': ['down', 'left', 'right'],
		'left': ['left', 'down', 'up'],
		'right': ['right', 'down', 'up']
	}

	# Utility function to check if a move is valid
	def is_valid_move(pos1, pos2, direction, i):
		valid_pos1 = valid_symbols[direction][i][0] | valid_symbols['universal']
		valid_pos2 = valid_symbols[direction][i][1] | valid_symbols['universal']
		return pos1 not in visited and pos2 not in visited and map[pos1[0]][pos1[1]] in valid_pos1 and map[pos2[0]][pos2[1]] in valid_pos2

	# Check and recurse for each possible move
	findings = set() 
	for idx, next_pos in enumerate(next_positions[direction]): 
		if not is_valid_position(map, next_pos): 
			continue
		if next_pos not in visited and is_valid_move(next_pos[0], next_pos[1], direction, idx):
			visited.add(next_pos)
			found = connect_to_other_cluster(map, network, *next_pos[0], *next_pos[1], next_direction[direction][idx], visited)
			if found: 
				findings = findings | found
	return findings 

def find_gaps(map, cluster, network):
	moves = []
	for i, j in cluster:
		positions = [((i-1, j-1), (i-1, j)), # up left
				((i-1, j), (i-1, j+1)), # up right
				((i+1, j-1), (i+1, j)), # down left
				((i+1, j), (i+1, j+1)), # down right
				((i, j-1), (i-1, j-1)), # left up
				((i+1, j-1), (i, j-1)), # left down
				((i, j+1), (i-1, j+1)), # right up
				((i+1, j+1), (i, j+1)) # right down
				]
		valid_values = [[['|', 'J', '7'], ['|', 'L', 'F']], 
				[['|', 'J', '7'], ['|', 'L', 'F']],
				[['|', 'J', '7'], ['|', 'L', 'F']],
				[['|', 'J', '7'], ['|', 'L', 'F']],
				[['-', 'F', '7'], ['-', 'J', 'L']],
				[['-', 'F', '7'], ['-', 'J', 'L']],
				[['-', 'F', '7'], ['-', 'J', 'L']],
				[['-', 'F', '7'], ['-', 'J', 'L']],
				]
		valid_values = [[set(val) for val in vals] for vals in valid_values]

		universal = set(['.', 'I'])
		i = -1
		for (pos_1, pos_2), valid_value in zip(positions, valid_values):
			i += 1
			if not is_valid_position(map, (pos_1, pos_2)): continue
			if pos_1 in cluster or pos_2 in cluster: continue
			if map[pos_1[0]][pos_1[1]] not in valid_value[0] | universal: continue
			if map[pos_2[0]][pos_2[1]] not in valid_value[1] | universal: continue
			if i < 2:
				direction = 'up'
			elif i < 4:
				direction = 'down'
			elif i < 6:
				direction = 'left'
			else:
				direction = 'right'
			moves.append(((pos_1, pos_2), direction))
	return moves

def merge_and_validate_cluster(map, network, cluster, visited, maybe_enclosed, not_enclosed):
	is_enclosed = True
	moves = find_gaps(map, cluster, network)
	while len(moves) > 0:
		(pos_1, pos_2), direction = moves.pop()
		visited.add((pos_1, pos_2))
		points = connect_to_other_cluster(map, network, pos_1[0], pos_1[1], pos_2[0], pos_2[1], direction, visited)
		for point in points:
			if any(point in cluster for cluster in not_enclosed):
				is_enclosed = False
			for i in range(len(maybe_enclosed)):
				if point in maybe_enclosed[i]:
					cluster = maybe_enclosed[i] | cluster
					visited = visited | maybe_enclosed[i]
					moves += find_gaps(map, maybe_enclosed[i], network)
					maybe_enclosed.pop(i)
					break
	if not is_enclosed:
		for i, j in cluster:
			map[i][j] = '.'

		
def part_2(network, map):
	clusters = []
	for i in range(len(map)):
		for j in range(len(map[i])):
			if (i, j) in network: continue
			if any((i, j) in visited for visited in clusters): continue
			clusters.append(fill_map(map, network, i, j, set([(i, j)])))
	# Mark all clusters that are definitely not enclosed	
	not_enclosed = [cluster for cluster in clusters if is_not_enclosed(map, cluster)]
	for cluster in not_enclosed:
		for i, j in cluster:
			map[i][j] = '.'
	# Mark all clusters that are maybe enclosed
	maybe_enclosed = [cluster for cluster in clusters if not is_not_enclosed(map, cluster)]
	for cluster in maybe_enclosed:
		for i, j in cluster:
			map[i][j] = 'I'
	# Save the 2D array to a txt file for inspection 
	np.savetxt('output.txt', map, fmt='%s')		

	# See if any of the maybe enclosed clusters are actually enclosed 
	visited = set()
	while len(maybe_enclosed) > 0: 
		cluster = maybe_enclosed.pop()
		visited |= set(cluster)
		merge_and_validate_cluster(map, network, cluster, visited, maybe_enclosed, not_enclosed)
			
	np.savetxt('output.txt', map, fmt='%s')		

	# Count the number of enclosed regions
	enclosed_regions = 0
	for i, row in enumerate(map):
		for j, val in enumerate(row):
			if val == '.': continue
			if (i, j) in network: continue
			enclosed_regions += 1
	return enclosed_regions

def main():
	map, network, start_position = parse_input('input.txt')
	#visualize_network(network)
	print("Part 1: ", part_1(network, start_position)) # 6773
	print("Part 2:", part_2(network, map)) # 493

if __name__ == '__main__':
	main()  