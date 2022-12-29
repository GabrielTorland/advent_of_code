from aocd import get_data
from collections import defaultdict
from heapq import heappush, heappop


def generate_states(horizontal, vertical, x_rng, y_rng, delta_x, delta_y):
	horizontal_states = [set(horizontal.keys())]
	state = horizontal
	for i in range(delta_x-1):
		new_state = defaultdict(lambda: defaultdict(int))
		for pos, blizzards in state.items():
			for type, count in blizzards.items():
				match type:
					case ">":
						new_state[((pos[0]-x_rng[0] + 1) % delta_x + x_rng[0], pos[1])][type] += count
					case "<":
						new_state[((pos[0] - x_rng[0] - 1) % delta_x + x_rng[0], pos[1])][type] += count
		horizontal_states.append(set(new_state.keys()))
		state = new_state
	vertical_states = [set(vertical.keys())]
	state = vertical
	for i in range(delta_y-1):
		new_state = defaultdict(lambda: defaultdict(int))
		for pos, blizzards in state.items():
			for type, count in blizzards.items():
				match type:
					case "^":
						new_state[(pos[0], (pos[1] - y_rng[0] - 1) % delta_y + y_rng[0])][type] += count
					case "v":
						new_state[(pos[0], (pos[1] - y_rng[0] + 1) % delta_y + y_rng[0])][type] += count	
		vertical_states.append(set(new_state.keys()))	
		state = new_state
	return horizontal_states, vertical_states


def parse(raw):
	lines = raw.splitlines()
	x_rng = (1, len(lines[0]) - 2)
	y_rng = (1, len(lines) - 2)
	delta_x, delta_y = x_rng[1] - x_rng[0] + 1, y_rng[1] - y_rng[0] + 1
	horizontal = defaultdict(lambda: defaultdict(int))
	vertical = defaultdict(lambda: defaultdict(int))
	for y, line in enumerate(lines):
		for x, entry in enumerate(line):
			match entry:
				case ">":
					horizontal[(x, y)][">"] += 1
				case "<":
					horizontal[(x, y)]["<"] += 1
				case "^":
					vertical[(x, y)]["^"] += 1
				case "v":
					vertical[(x, y)]["v"] += 1
	return horizontal, vertical, x_rng, y_rng, delta_x, delta_y		


# Dijkstra's algorithm
def shortest_path(horizontal_states, vertical_states, x_rng, y_rng, delta_x, delta_y, start, goal, t0):
	heap = []
	visited = set()
	heappush(heap, (t0, start))
	visited.add((t0, start))
	while heap:
		time, pos = heappop(heap)
		if pos == goal:
			return time
		new_state = horizontal_states[(time+1) % delta_x] | vertical_states[(time+1) % delta_y]
		for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]:
			new_pos = (pos[0] + x, pos[1] + y)
			if new_pos in new_state: continue
			if ((x_rng[0] <= new_pos[0] <= x_rng[1]) and (y_rng[0] <= new_pos[1] <= y_rng[1]) or new_pos in [goal, start]):
				if (time + 1, new_pos) in visited: continue
				heappush(heap, (time + 1, new_pos))
				visited.add((time + 1, new_pos))
	return -1


if __name__ == "__main__":
	raw = get_data(day=24, year=2022)
	horizontal, vertical, x_rng, y_rng, delta_x, delta_y = parse(raw)
	horizontal_states, vertical_states = generate_states(horizontal, vertical, x_rng, y_rng, delta_x, delta_y)
	start = (1, 0)
	goal = (x_rng[1], y_rng[1]+1)
	t1 = shortest_path(horizontal_states, vertical_states, x_rng, y_rng, delta_x, delta_y, start, goal, 0)
	t2 = shortest_path(horizontal_states, vertical_states, x_rng, y_rng, delta_x, delta_y, goal, start, t1) 
	t3 = shortest_path(horizontal_states, vertical_states, x_rng, y_rng, delta_x, delta_y, start, goal, t2)
	print("Part 2: ", t3) # 839

