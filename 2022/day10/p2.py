from aocd import get_data

def calc_signal_strengths(instructions):
	# storing the instructions with the associated starting cycle
	oper = []
	for instruction in instructions:
		match instruction.split():
			case ["noop", *_]:
				oper.append((0, 2 if len(oper) == 0 else oper[-1][1] + 1))
			case ["addx", rest]:
				oper.append((int(rest), 3 if len(oper) == 0 else oper[-1][1] + 2))
	
	signal_strengths = []
	cycle = 1
	# current signal strength
	X = 1
	# list of string containing the pattern we are asked to find
	patter = []
	# tmp string that is appended to patter, i.e., a row of the pattern
	row = ""
	while len(oper) > 0:
		# Check if the spite is on the current entry 
		if X <= len(row)+1 <= X + 2:
			row += "#"
		else:
			row += "."
		cycle += 1
		# check if we are done with the current instruction, move to the next one
		if cycle == oper[0][1]:
			X += oper.pop(0)[0]
		if cycle in [41, 81, 121, 161, 201, 241]:
			signal_strengths.append(X*cycle)
			patter.append(row)
			row = ""
	return signal_strengths, patter

if __name__ == '__main__':
	inst = get_data(day=10, year=2022).splitlines()
	signal_strengths, pattern = calc_signal_strengths(inst)
	print("Part 2: ")
	for line in pattern: print(line)
