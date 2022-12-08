import sys
from aocd import get_data, submit

def science_scores(data):
	scores = []
	for y in range(0, len(data)):
		for x in range(0, len(data[y])):
			score = 1
			# up
			su = 0
			for _y in range(y-1, -1, -1):
				su += 1
				if data[_y][x] >= data[y][x]:
					break
			# down
			sd = 0
			for _y in range(y+1, len(data)):
				sd += 1
				if data[_y][x] >= data[y][x]:
					break
			# left
			sl = 0
			for _x in range(x-1, -1, -1):
				sl += 1
				if data[y][_x] >= data[y][x]:
					break
			# right
			sr = 0
			for _x in range(x+1, len(data[y])):
				sr += 1
				if data[y][_x] >= data[y][x]:
					break	
			scores.append(sr*sl*su*sd)
	return scores
	
if __name__ == '__main__':
	data = [[int(c) for c in line] for line in get_data(day=8, year=2022).split('\n')]
	# data = [[int(c) for c in line ] for line in open("test.in").read().split('\n')]
	scores = science_scores(data)
	ans = max(scores)
	print(ans)
	submit_ = input('Submit? (y/n)')
	if submit_ == 's':
		print(submit(ans), part="b", day=8, year=2022)