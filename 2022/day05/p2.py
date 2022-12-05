import sys
from collections import defaultdict 

def parse():
	data = open(sys.argv[1] if len(sys.argv) > 1 else "input.in", 'r').read().split("\n\n")
	
	creates = defaultdict(list)
	tmp = data[0].split("\n")
	for l in tmp[:len(tmp)-1]:
		for i in range(1, len(l), 4):
			if l[i] == ' ': continue
			creates[i//4].append(l[i])

	instructions = [[l.split(' ')[1], l.split(' ')[3], l.split(' ')[5]] for l in data[1].split("\n")]
	return creates, instructions

def move(n, s, d, creates):
	creates[d] = creates[s][:n] + creates[d]
	creates[s] = creates[s][n:]

def on_top(creates):
	return [val[0] for key, val in sorted(creates.items(), key=lambda x: x[0])]	

if __name__ == '__main__':
	creates, instructions = parse()
	for n, s, d in instructions:
		move(int(n), int(s)-1, int(d)-1, creates)
	print("Part 2: ", "".join(on_top(creates)))