import heapq

def parse(input_file):
	return [entry for entry in open(input_file).read().splitlines()]

def get_start_and_finish_positions(maze):
	for i, row in enumerate(maze):
		for j, entry in enumerate(row):
			if entry == "S":
				start = (i, j)
			elif entry == "E":
				finish = (i, j)
	return start, finish

def shortest_path(maze, start, finish, direction, stop_if_found):
	heap = []
	# Initialize the heap with the starting position
	# combine start tuple and direction to a 3-tuple
	heapq.heappush(heap, (0, start+ (direction,), {start+(direction,)}))

	optimal_cost = float("inf")
	optimal_tiles = set()
	position_cost = {}
	while heap:
		cost, current, path = heapq.heappop(heap)

		i, j, direction = current

		position_cost[(i, j, direction)] = cost

		# If finish is reached, return the path
		if (i, j) == finish and cost <= optimal_cost:
			optimal_cost = cost
			if stop_if_found:
				return cost, path
			else:
				path_only_positions = {pos[:2] for pos in path}
				optimal_tiles = optimal_tiles.union(path_only_positions)
				continue

		for current_move, cost_move in get_possible_moves(maze, (i, j), direction):
			if not stop_if_found:
				if (cost + cost_move) >= position_cost.get(current_move, float("inf")):
					continue
			else:
				if (cost + cost_move) > position_cost.get(current_move, float("inf")):
					continue
			if current_move in path:
				continue
			heapq.heappush(heap, (cost+cost_move, current_move, path.union({current_move})))

	return optimal_cost, optimal_tiles

def get_possible_moves(maze, position, direction):
	moves = []
	i, j = position
	direction_map = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

	# Move from current position in the current direction
	di, dj = direction_map[direction]
	ni, nj = i + di, j + dj
	# Ensure new position is within maze bounds
	if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]):
		# Check if the new position is not a wall
		if maze[ni][nj] != "#":
			moves.append(((ni, nj, direction), 1))

	# Rotate 90 degrees to the right, but keep the same position
	moves.append(((i, j, (direction + 1) % 4), 1000))
	# Rotate 90 degrees to the left, but keep the same position
	moves.append(((i, j, (direction - 1) % 4), 1000))

	return moves

if __name__ == "__main__":
	maze = parse("input.txt")
	start, finish = get_start_and_finish_positions(maze)
	optimal_cost, _ = shortest_path(maze, start, finish, 1, True)
	print("Part 1:", optimal_cost)
	_, optimal_tiles = shortest_path(maze, start, finish, 1, False)
	print("Part 2: ", len(optimal_tiles))
