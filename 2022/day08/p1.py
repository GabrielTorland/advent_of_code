import sys
from aocd import get_data, submit

def visible_trees(data):
	visible = set()
	unknown = set()	
	for y in range(1, len(data)-1):
		t = -1
		for x, col in enumerate(data[y]):
			if col <= t: continue
			t = col
			visible.add((x, y))
		t = -1	
		for x in range(len(data[y+1])-1, -1, -1):
			if data[y][x] <= t and (x, y) not in visible:
				unknown.add((x, y))
				continue
			t = data[y][x]
			visible.add((x, y))
	
	
	for x, y in unknown:
		vis = True 
		for _y in range(y-1, -1, -1):
			if data[_y][x] >= data[y][x]:
				vis = False
				break
		if vis: visible.add((x, y))
		else:
			vis = True
			for _y in range(y+1, len(data)):
				if data[_y][x] >= data[y][x]:
					vis = False
					break
			if vis: visible.add((x, y))
	return visible.union(*[set((i, 0)for i in range(len(data[0]))), set((i, len(data)) for i in range(len(data[-1])))])

	
if __name__ == '__main__':
	data = [[int(c) for c in line] for line in get_data(day=8, year=2022).split('\n')]
	# data = [[int(c) for c in line ] for line in open("test.in").read().split('\n')]
	visible = visible_trees(data)
	ans = len(visible)	
	print(ans)
	submit_ = input('Submit? (y/n)')
	if submit_ == 's':
		print(submit(ans), part="a", day=8, year=2022)
		