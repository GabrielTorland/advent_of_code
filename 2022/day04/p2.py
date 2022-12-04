import sys

def is_subset(r_1, r_2):
	if r_1[0] >= r_2[0] and (r_1[1] <= r_2[1] or r_1[0] <= r_2[1]):
		return 1
	elif r_1[0] <= r_2[0] and (r_1[1] >= r_2[1] or r_1[1] >= r_2[0]):
		return 1
	else:
		return 0

if __name__ == '__main__':
	input = [[tuple(int(n) for n in s.split("-")) for s in l.split(',')] for l in open(sys.argv[1] if len(sys.argv) > 1 else 'input.in').read().split("\n")]
	print("Part 2: ", sum([is_subset(r[0], r[1]) for r in input]))