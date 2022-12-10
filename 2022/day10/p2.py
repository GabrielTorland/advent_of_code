from aocd import get_data

def find_pattern(instructions):
	cycles = 1
	sign_strengths = []
	X = 1
	pattern = []
	row = ""
	for i in instructions:
		match i.split():
			case ["noop", *_]:
				if X <= len(row)+1 <= X + 2:
					row += "#"
				else:
					row += "."
				cycles += 1
				if cycles in [41, 81, 121, 161, 201, 241]: 
					sign_strengths.append(X*cycles)
					pattern.append(row)
					row = ""
			case ["addx", val]:
				if X <= len(row)+1 <= X + 2:
					row += "#"
				else:
					row += "."
				cycles += 1
				if cycles in [41, 81, 121, 161, 201, 241]:
					sign_strengths.append(X*cycles)
					pattern.append(row)
					row = ""
				if X <= len(row)+1 <= X + 2:
					row += "#"
				else:
					row += "."
				cycles += 1
				X += int(val)				
				if cycles in [41, 81, 121, 161, 201, 241]:
					sign_strengths.append(X*cycles)
					pattern.append(row)
					row = ""
	return sign_strengths, pattern

if __name__ == '__main__':
	instructions = get_data(day=10, year=2022).splitlines()
	signal_strengths, pattern = find_pattern(instructions)
	print("Part 2: ")
	for line in pattern: print(line)
