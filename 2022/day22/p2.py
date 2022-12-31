from aocd import get_data
import re
import regex_spm
from copy import deepcopy

class Entry:
	def __init__(self, val, x, y, left, right, up, down):
		self.x, self.y = x, y
		self.val = val
		self.left = left
		self.right = right
		self.up = up
		self.down = down
		self.dir_changes = {0: 0, 1: 0, 2: 0, 3: 0}

	def __eq__(self, __o: object) -> bool:
		return self.x == __o.x and self.y == __o.y
	
class Plane:
	def __init__(self, id, corner, size) -> None:
		self.id = id 
		self.corner = corner
		self.edge_up = [corner]
		self.edge_left = [corner] 
		# upmost edge
		current = corner
		for _ in range(size-1):
			current = current.right
			self.edge_up.append(current)
		# leftmost edge
		current = corner
		for _ in range(size-1):
			current = current.down
			self.edge_left.append(current)
		self.edge_right = [self.edge_up[-1]]
		self.edge_down = [self.edge_left[-1]]
		# rightmost edge
		current = self.edge_up[-1]
		for _ in range(size-1):
			current = current.down
			self.edge_right.append(current)
		# downmost edge
		current = self.edge_left[-1]
		for _ in range(size-1):
			current = current.right
			self.edge_down.append(current)


def in_edges(corner, planes, exclude):
	for plane in planes:
		if plane.id == exclude: continue
		if corner in (plane.edge_up + plane.edge_left + plane.edge_right + plane.edge_down):
			return True
	return False

def in_board(x, y, max_x, max_y):
	return 0 <= x <= max_x and 0 <= y <= max_y

def connect_edges(planes):
	"""
	This is a bit of a mess, but it works.
	The connections are determined by manually checking the data.
	Propably a better way that is more generic, so pleas let me know if you find it.
	"""

	
	plane = planes[0]
	for e1, e2 in zip(plane.edge_left, planes[3].edge_left[::-1]):
		e1.left = e2
		e1.dir_changes[2] = 2
		e2.left = e1
		e2.dir_changes[2] = 2
	for e1, e2 in zip(plane.edge_up, planes[5].edge_left):
		e1.up = e2
		e1.dir_changes[3] = 1
		e2.left = e1
		e2.dir_changes[2] = -1
	plane = planes[1]
	for e1, e2 in zip(plane.edge_down, planes[2].edge_right):
		e1.down = e2
		e1.dir_changes[1] = 1
		e2.right = e1
		e2.dir_changes[0] = 3
	for e1, e2 in zip(plane.edge_right, planes[4].edge_right[::-1]):
		e1.right = e2
		e1.dir_changes[0] = 2
		e2.right = e1
		e2.dir_changes[0] = 2
	for e1, e2 in zip(plane.edge_up, planes[5].edge_down):
		# direction is unchanged
		e1.up = e2
		e2.down = e1
	plane = planes[2]
	for e1, e2 in zip(plane.edge_left, planes[3].edge_up):
		e1.left = e2
		e1.dir_changes[2] = -1
		e2.up = e1
		e2.dir_changes[3] = 1
	# already connected plane 3
	plane = planes[4]
	for e1, e2 in zip(plane.edge_down, planes[5].edge_right):
		e1.down = e2
		e1.dir_changes[1] = 1
		e2.right = e1
		e2.dir_changes[0] = 3


def parse(raw, size):
	raw_board, instructions = raw.split('\n\n')
	board = {}
	for i, line in enumerate(raw_board.splitlines()):
		for j, c in enumerate(line):
			if c == ' ': continue
			board[(i, j)] = Entry(c, j, i, (i, j-1), (i, j+1), (i-1, j), (i+1, j))
		

	# updating the neigbors to pointers
	# accounting for the wrapping on the edges
	tmp_planes = [[] for _ in range(6)]
	ranges = []
	new_board = deepcopy(board)
	max_x = 0
	max_y = 0
	for entry in board.values():
		added = False
		for i, rng in enumerate(ranges):
			if rng[0] <= entry.x <= rng[1] and rng[2] <= entry.y <= rng[3]:
				if entry.x == rng[0] or entry.x == rng[1] or entry.y == rng[2] or entry.y == rng[3]:
					tmp_planes[i].append(new_board[(entry.y, entry.x)])
				added = True
				break
		if not added:
			ranges.append([entry.x, entry.x + size-1, entry.y, entry.y + size-1])
			tmp_planes[len(ranges)-1].append(new_board[(entry.y, entry.x)])
		if entry.left in board:
			new_board[(entry.y, entry.x)].left = new_board[entry.left]
		if entry.right in board:
			new_board[(entry.y, entry.x)].right = new_board[entry.right]
		if entry.up in board:
			new_board[(entry.y, entry.x)].up = new_board[entry.up]
		if entry.down in board:
			new_board[(entry.y, entry.x)].down = new_board[entry.down]
		max_x = max(max_x, entry.x)
		max_y = max(max_y, entry.y)

	# creating the planes
	planes = []
	i = 0
	while len(tmp_planes) > 0:
		plane = tmp_planes.pop(0)
		planes.append(Plane(i, plane[0], size))
		i += 1
	connect_edges(planes)
	return new_board, re.findall(r"(\d+|L|R)", instructions.strip()), list(new_board.values())[0]

def move_left(current):
	return current.left

def move_right(current):
	return current.right

def move_up(current):
	return current.up

def move_down(current):
	return current.down

def decide_move(dir):
	match dir:
		case 0:
			return move_right
		case 1:
			return move_down
		case 2:
			return move_left
		case 3:
			return move_up
		case _:
			raise ValueError(f"Unknown move direction {dir}")

def follow_instructions(board, instructions, start):		
	# direction: 0 = right, 1 = down , 2 = left, 3 = up 
	dir = 0
	current = start
	for instruction in instructions:
		match regex_spm.fullmatch_in(instruction):
			case r'R':
				# clockwise
				dir = (dir + 1) % 4
			case r'L':
				# counter-clockwise
				dir = (dir - 1) % 4
			case r"\d+":
				move = decide_move(dir)	
				for _ in range(int(instruction)):
					tmp = move(current) 
					if tmp.val == '#': 
						break
					new_dir = (dir + current.dir_changes[dir]) % 4
					# update the direction if it changes in a transition between two planes
					if new_dir != dir:
						dir = new_dir
						move = decide_move(dir)
					current = tmp
			case _:
				raise ValueError(f"Unknown instruction {instruction}")
	return current.x+1, current.y+1, dir

	


if __name__ == '__main__':
	raw = get_data(day=22, year=2022)
	board, instructions, start = parse(raw, 50)
	x, y, dir = follow_instructions(board, instructions, start) # 184106
	print("Part 2:", 1000*y + 4*x + dir)

