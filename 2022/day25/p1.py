from aocd import get_data

def snafu_2_base10(snafu: str) -> int:
	"""Convert a snafu number to base 10."""
	base10 = 0
	for i, digit in enumerate(snafu[::-1]):
		match digit:
			case '0' | '1' | '2':
				base10 += int(digit)*5**i
			case '-':
				base10 -= 5**i
			case '=':
				base10 -= 2*5**i
	return base10

def base10_2_snafu(base10: int) -> str:
	"""Convert a base 10 number to snafu."""
	snafu = ''
	while base10:
		rest = 0
		match base10 % 5:
			case 0:
				snafu += '0'
			case 1:
				snafu += '1'
			case 2:
				snafu += '2'
			case 3:
				rest = 1
				snafu += '='
			case 4:
				rest = 1
				snafu += '-'
		base10 //= 5
		base10 += rest
		rest = 0
	return snafu[::-1]


if __name__ == '__main__':
	snafu_numbers = get_data(day=25, year=2022).splitlines()
	base10_numbers = [snafu_2_base10(snafu) for snafu in snafu_numbers]
	num = sum(base10_numbers)
	print(num)
	print("Part 1: ", base10_2_snafu(num))

