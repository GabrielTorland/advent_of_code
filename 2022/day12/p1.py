from aocd import get_data
from heapq import heappush, heappop, heapify 


def get_neighbors(maze, current):
	neighbors = []
	if current[0] < len(maze) - 1:
		neighbors.append((current[0] + 1, current[1]))
	if current[0] > 0:
		neighbors.append((current[0] - 1, current[1]))
	if current[1] < len(maze[0]) - 1:
		neighbors.append((current[0], current[1] + 1))
	if current[1] > 0:
		neighbors.append((current[0], current[1] - 1))
	return neighbors


def valid(maze, current, neighboor):
	return (ord(maze[neighboor[0]][neighboor[1]]) - ord(maze[current[0]][current[1]])) <= 1

def generate_path(maze, parent, current):
	prev = None
	current = current
	while current is not None:
		if prev is None:
			maze[current[0]][current[1]] = 'E'
		elif prev[0] < current[0]:
			maze[current[0]][current[1]] = '^'
		elif prev[0] > current[0]:
			maze[current[0]][current[1]] = 'v'
		elif prev[1] < current[1]:
			maze[current[0]][current[1]] = '<'
		else:
			maze[current[0]][current[1]] = '>'
		prev = current
		current = parent[current]
	with open("out.txt", "w") as f:
		for line in maze:
			f.write(", ".join(c for c in line))
			f.write("\n")

# Dijkstra's algorithm for shortest path
# Utilizing a heap
def shortest_path(maze, start, goal):
	# The heap
	heap = [((0, start))]
	heapify(heap)

	# The visited set
	visited = set()

	# The parent dict
	parent = {}
	parent[start] = None

	queue = {start: 0}

	while len(heap) > 0:
		# Get the shortest path
		steps, current = heappop(heap)

		# If we've reached the goal, we're done
		if current == goal:
			generate_path(maze, parent, current)
			return steps

		if maze[current[0]][current[1]] == 't':
			print()
		visited.add(current)
		del queue[current] 

		# Get the neighbors
		neighbors = get_neighbors(maze, current)

		# Loop through the neighbors
		for neighbor in neighbors:
			# If it's not valid, continue
			if not valid(maze, current, neighbor):
				continue

			# If we've already visited it, continue
			if neighbor in visited:
				continue

			# If it's in the queue and the steps are less than the current steps, continue
			if neighbor in queue.keys() and queue[neighbor] <= steps + 1:
				continue

			parent[neighbor] = current
			heappush(heap, (steps + 1, neighbor))
			queue[neighbor] = steps + 1
		if len(queue) == 0:
			return "No path found"


def find_star_and_goal(maze):
	s = "S"
	start = None
	g = "E"
	goal = None
	for i, line in enumerate(maze):
		if s in line:
			start = (i, line.index(s))

		if g in line:
			goal = (i, line.index(g))
	return start, goal


if __name__ == '__main__':
	maze = [[entry for entry in row] for row in get_data(day=12, year=2022).splitlines()]   
	s, g = find_star_and_goal(maze)
	maze[s[0]][s[1]] = 'a'
	maze[g[0]][g[1]] = 'z'
	print("Part 1: ", shortest_path(maze, s, g))