from aocd import get_data
import numpy as np

def draw_or_not(X, i):
	c = None 
	if X <= i <= X + 2:
		c = "#"
	else:
		c = "."
	return c

def print_pattern(pattern):
	for row in pattern:
		for entry in row:
			print(entry.decode("utf-8"), end=" ")
		print()

def next_row(row):
	return row + 1, 0


def find_pattern(instructions):
	cycles = 1
	sign_strengths = []
	X = 1
	pattern = np.chararray((6, 40))
	row, col = 0, 0
	for i in instructions:
		match i.split():
			case ["noop", *_]:
				pattern[row][col] = draw_or_not(X, col+1);col += 1
				cycles += 1
				if (cycles-1) % 40 == 0:
					sign_strengths.append(X*cycles)
					row, col = next_row(row)

			case ["addx", val]:
				pattern[row][col] = draw_or_not(X, col+1);col += 1	
				cycles += 1
				if (cycles-1) % 40 == 0:
					sign_strengths.append(X*cycles)
					row, col = next_row(row)
				pattern[row][col] = draw_or_not(X, col+1);col += 1
				cycles += 1
				X += int(val)				
				if (cycles-1) % 40 == 0:
					sign_strengths.append(X*cycles)
					row, col = next_row(row)
	return sign_strengths, pattern

if __name__ == '__main__':
	instructions = get_data(day=10, year=2022).splitlines()
	signal_strengths, pattern = find_pattern(instructions)
	print("Part 2: ")
	print_pattern(pattern)
