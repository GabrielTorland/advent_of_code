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


def parse(raw):
	raw_board, instructions = raw.split('\n\n')
	board = {}
	for i, line in enumerate(raw_board.splitlines()):
		for j, c in enumerate(line):
			if c == ' ': continue
			board[(i, j)] = Entry(c, j, i, (i, j-1), (i, j+1), (i-1, j), (i+1, j))

	# updating the neigbors to pointers
	# accounting for the wrapping on the edges
	new_board = deepcopy(board)
	for entry in board.values():
		if entry.left not in board:
			current = entry 
			while current.right in board:
				current = board[current.right]
			new_board[(entry.y, entry.x)].left = new_board[(current.y, current.x)]
		else:
			new_board[(entry.y, entry.x)].left = new_board[entry.left]
		if entry.right not in board:
			current = entry
			while current.left in board:
				current = board[current.left]
			new_board[(entry.y, entry.x)].right = new_board[(current.y, current.x)]
		else:
			new_board[(entry.y, entry.x)].right = new_board[entry.right]
		if entry.up not in board:
			current = entry
			while current.down in board:
				current = board[current.down]
			new_board[(entry.y, entry.x)].up = new_board[(current.y, current.x)]
		else:
			new_board[(entry.y, entry.x)].up = new_board[entry.up]
		if entry.down not in board:
			current = entry
			while current.up in board:
				current = board[current.up]
			new_board[(entry.y, entry.x)].down = new_board[(current.y, current.x)]
		else:
			new_board[(entry.y, entry.x)].down = new_board[entry.down]
	return new_board, re.findall(r"(\d+|L|R)", instructions.strip()), list(new_board.values())[0]

def move_left(current):
	return current.left

def move_right(current):
	return current.right

def move_up(current):
	return current.up

def move_down(current):
	return current.down


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
				match dir:
					case 0:
						move = move_right
					case 1:
						move = move_down
					case 2:
						move = move_left
					case 3:
						move = move_up
				for _ in range(int(instruction)):
					tmp = move(current) 
					if tmp.val == '#': break
					current = tmp
			case _:
				raise ValueError(f"Unknown instruction {instruction}")
	return current.x+1, current.y+1, dir

	


if __name__ == '__main__':
	raw = get_data(day=22, year=2022)
	board, instructions, start = parse(raw)
	x, y, dir = follow_instructions(board, instructions, start) # 30552
	print("Part 1:", 1000*y + 4*x + dir)

