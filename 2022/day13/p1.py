from aocd import get_data
import json

def comp_elems(a, b, n):
	for i in range(min(len(a), len(b))):
		e1, e2 = a[i], b[i]
		# both elements are ints
		if isinstance(e1, int) and isinstance(e2, int):
			if e1 > e2: return 0
			elif e1 < e2: return n 
		# element 1 is an int and element 2 is a list
		elif isinstance(e1, int) and isinstance(e2, list): 
			state = comp_elems([e1], e2, n)
			if state == 0: return 0
			elif state == n: return n 
		# element 1 is a list and element 2 is an int
		elif isinstance(e1, list) and isinstance(e2, int): 
			state = comp_elems(e1, [e2], n)
			if state == 0: return 0
			elif state == n: return n 
		# both elements are lists
		elif isinstance(e1, list) and isinstance(e2, list): 
			state = comp_elems(e1, e2, n)
			if state == 0: return 0
			elif state == n: return n 
	if len(a) == len(b):
		return -1
	elif len(a) < len(b):
		return n
	else:
		return 0

if __name__ == '__main__':
	data = [[json.loads(elem) for elem in pair.split('\n')] for pair in get_data(day=13, year=2022).split("\n\n")]
	right_order = 0
	for i, pair in enumerate(data):
		right_order += comp_elems(pair[0], pair[1], i+1)
	print("Part 1: ", right_order)
