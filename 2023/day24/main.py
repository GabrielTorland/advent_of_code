from sympy import symbols, linsolve, solve
from functools import lru_cache
import re

class Hailstone:
	def __init__(self, x, y, z, vx, xy, vz) -> None:
		self.x = x
		self.y = y
		self.z = z
		self.vx = vx
		self.vy = xy
		self.vz = vz

		self.xy_equation = self.__get_xy_line_equation()
		self.in_past_equation = self.__get_in_past_equation()

	def __get_in_past_equation(self):
		x, t = symbols('x t')
		x_t = self.x + t*self.vx

		# Solve for t
		t_solution = solve(x_t - x, t)[0]

		return t_solution

	def __get_xy_line_equation(self):
		x, y, t = symbols('x y t')
		x_t = self.x + t*self.vx
		y_t = self.y + t*self.vy

		# Solve for t	
		t_solution = solve(x_t - x, t)

		# Substitute t in y equation
		y_in_terms_of_x = y_t.subs(t, t_solution[0])

		# Remove y to get equal to 0
		x_y_equation = y_in_terms_of_x - y

		return x_y_equation
	
	def in_past(self, x_val):
		t = self.in_past_equation.subs('x', x_val)
		return t < 0

	def find_intersection_point(self, other):
		x, y = symbols('x y')

		intersection = list(linsolve([self.xy_equation, other.xy_equation], x, y))
		return intersection[0]
	


def parse(input_path='input.txt'):
	hailstones = []
	for line in open(input_path).read().splitlines():
		hailstones.append(Hailstone(*map(int, re.findall(r'-?\d+', line))))
	return hailstones 


def find_intersections_within_bounds(hailstones, min_val=200000000000000, max_val=400000000000000):
	intersections = []
	for i in range(len(hailstones)):
		for j in range(i+1, len(hailstones)):
			# Skip if the hailstones move in parallel
			if hailstones[i].vx*hailstones[j].vy == hailstones[i].vy*hailstones[j].vx:
				continue
			# Find intersection point
			intersection = hailstones[i].find_intersection_point(hailstones[j])
			x_val, y_val = map(float, intersection)

			# Skip if the intersection point is in the past
			if hailstones[i].in_past(x_val) or hailstones[j].in_past(x_val):
				continue

			# Check if the intersection point is within bounds
			if min_val <= x_val <= max_val and min_val <= y_val <= max_val:
				intersections.append((x_val, y_val))
	return intersections

def part_2(hailstones):
	xr, yr, zr, vxr, vyr, vzr = symbols('xr yr zr vxr vyr vzr')

	equations = []	

	for hs in hailstones:
		equations.append((xr - hs.x) * (hs.vy - vyr) - (yr - hs.y) * (hs.vx - vxr))
		equations.append((yr - hs.y)*(hs.vz - vzr) - (zr - hs.z)*(hs.vy - vyr))
	answer = solve(equations)[0]
	return answer[xr]+answer[yr]+answer[zr]

if __name__ == '__main__':
	hailstones = parse()
	print("Part 1: ", len(find_intersections_within_bounds(hailstones)))
	print("Part 2: ", part_2(hailstones))