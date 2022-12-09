import sys
from aocd import get_data

def move_knot(head, _tail):
	tail = _tail.copy()
	# Diagonal up right
	if ((head[0] - tail[0]) == -2) and ((head[1] - tail[1]) == 1):
		tail[0] -= 1
		tail[1] += 1
	elif ((head[0] - tail[0]) == -1) and ((head[1] - tail[1]) == 2):
		tail[0] -= 1
		tail[1] += 1
	elif ((head[0] - tail[0]) == -2) and ((head[1] - tail[1]) == 2):
		tail[0] -= 1
		tail[1] += 1
	# Diagonal up left
	elif ((head[0] - tail[0]) == -2) and ((head[1] - tail[1]) == -1):
		tail[0] -= 1
		tail[1] -= 1
	elif ((head[0] - tail[0]) == -1) and ((head[1] - tail[1]) == -2):
		tail[0] -= 1
		tail[1] -= 1
	elif ((head[0] - tail[0]) == -2) and ((head[1] - tail[1]) == -2):
		tail[0] -= 1
		tail[1] -= 1
	# Diagonal down right
	elif ((head[0] - tail[0]) == 2) and ((head[1] - tail[1]) == 1):
		tail[0] += 1
		tail[1] += 1
	elif ((head[0] - tail[0]) == 1) and ((head[1] - tail[1]) == 2):
		tail[0] += 1
		tail[1] += 1
	elif ((head[0] - tail[0]) == 2) and ((head[1] - tail[1]) == 2):
		tail[0] += 1
		tail[1] += 1
	# Diagonal down left
	elif ((head[0] - tail[0]) == 2) and ((head[1] - tail[1]) == -1):
		tail[0] += 1
		tail[1] -= 1
	elif ((head[0] - tail[0]) == 1) and ((head[1] - tail[1]) == -2):
		tail[0] += 1
		tail[1] -= 1
	elif ((head[0] - tail[0]) == 2) and ((head[1] - tail[1]) == -2):
		tail[0] += 1
		tail[1] -= 1
	# Down
	elif head[0] - tail[0] == 2:
		tail[0] += 1
	# Up
	elif head[0] - tail[0] == -2:
		tail[0] -= 1
	# Right
	elif head[1] - tail[1] == 2:
		tail[1] += 1
	# Left
	elif head[1] - tail[1] == -2:
		tail[1] -= 1
	return tail


def move_rope(instructions):
	head = [0, 0]
	inter_knots = [[0, 0]]*9
	visited = set().intersection((0, 0))
	for instruction in instructions:
		delta_x, delta_y = 0, 0
		match instruction.split(' '):
			case ['U', rest]:
				delta_y -= int(rest)
			case ['D', rest]:
				delta_y += int(rest)
			case ['L', rest]:
				delta_x -= int(rest)
			case ['R', rest]:
				delta_x += int(rest)
		if delta_y:
			for i in [-1 if delta_y < 0 else 1]*abs(delta_y):
				head[0] += i
				current_head = head
				for j, knot in enumerate(inter_knots):
					inter_knots[j] = move_knot(current_head, knot)
					current_head = inter_knots[j]
				visited.add((inter_knots[-1][0], inter_knots[-1][1]))
		else:
			for i in [-1 if delta_x < 0 else 1]*abs(delta_x):
				head[1] += i
				current_head = head
				for j, knot in enumerate(inter_knots):
					inter_knots[j] = move_knot(current_head, knot)
					current_head = inter_knots[j]
				visited.add((inter_knots[-1][0], inter_knots[-1][1]))
	return visited, head, inter_knots[-1]
				

if __name__ == '__main__':
	instructions = get_data(day=9, year=2022).splitlines()
	visited, head, tail =  move_rope(instructions)
	print(len(visited))