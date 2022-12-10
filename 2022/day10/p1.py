from aocd import get_data

def calc_signal_strengths(inst):
	# storing the instructions with the associated starting cycle
	oper = []
	for i in inst:
		match i.split():
			case ["noop", *_]:
				oper.append((0, 2 if len(oper) == 0 else oper[-1][1] + 1))
			case ["addx", rest]:
				oper.append((int(rest), 3 if len(oper) == 0 else oper[-1][1] + 2))
	
	sign_strengths = []
	cycle = 1
	# current signal strength
	X = 1
	while len(oper) > 0:
		cycle += 1
		# check if we are done with the current instruction, move to the next one
		if cycle == oper[0][1]:
			X += oper.pop(0)[0]
		if cycle in [20, 60, 100, 140, 180, 220]:
			sign_strengths.append(X*cycle)
	return sign_strengths

if __name__ == '__main__':
	inst = get_data(day=10, year=2022).splitlines()
	print("Part 1: ", sum(calc_signal_strengths(inst)))
