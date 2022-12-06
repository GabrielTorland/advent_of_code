import sys

def sofp_marker(s):
	uniques = 0
	v = []
	for i, c in enumerate(s):
		if c not in v:
			uniques += 1
			v.append(c)
		else:
			ind = v.index(c)
			uniques -= ind+1
			v = v[ind+1:]
			v.append(c)
			uniques += 1
		
		if uniques == 14:
			return i+1
	raise Exception("No 14 unique characters found")

if __name__ == '__main__':
	input = open(sys.argv[1] if len(sys.argv) > 1 else 'input.in').read()
	print("Part 2: ", sofp_marker(input))
