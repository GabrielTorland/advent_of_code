from aocd import get_data

def calc_signal_strengths(instructions):
	cycles = 1
	sign_strengths = []
	X = 1
	for i in instructions:
		match i.split():
			case ["noop", *_]:
				cycles += 1
				if (cycles-20) % 40 == 0: sign_strengths.append(X*cycles)
			case ["addx", val]:
				X += int(val)
				cycles += 1
				if (cycles-20) % 40 == 0: sign_strengths.append((X-int(val))*cycles)
				cycles += 1
				if (cycles-20) % 40 == 0:sign_strengths.append(X*cycles)

	return sign_strengths

if __name__ == '__main__':
	instructions = get_data(day=10, year=2022).splitlines()
	print("Part 1: ", sum(calc_signal_strengths(instructions)))
