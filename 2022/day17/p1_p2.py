from aocd import get_data
import numpy as np
import matplotlib.pyplot as plt

class Pile:
	def __init__(self, rounds) -> None:
		self.height = 0
		self.pile = np.chararray((4*rounds, 7), unicode=True)
		self.pile[:] = '.'

	def draw(self, rock):
		for delta_x, delta_y in rock.parts:
			self.pile[rock.y + delta_y][rock.x + delta_x] = '#'
		
	def get_entry(self, x, y):
		return self.pile[y][x]
	
	
class Rock:
	def __init__(self, parts) -> None:
		self.s = min(parts, key=lambda x: x[1])
		self.l = max(parts, key=lambda x: x[1])
		# inial position
		# position relative to the leftmost block 
		self.x, self.y = 2, -self.s[1] + 3
		self.parts = parts
		self.left, self.right, self.down = self.__determine_sides(parts)
		self.min_x, self.max_x, self.min_y = min(self.left, key=lambda x: x[0])[0], max(self.right, key=lambda x: x[0])[0], min(self.down, key=lambda x: x[1])[1]

	def __determine_sides(self, parts):
		# up is not important
		left, right, down = [], [], [] 
		for i in range(min(parts, key=lambda x: x[1])[1], max(parts, key=lambda x: x[1])[1] + 1):
			row = [part for part in parts if part[1] == i]
			left.append(min(row, key=lambda x: x[0]))
			right.append(max(row, key=lambda x: x[0]))
		for i in range(min(parts, key=lambda x: x[0])[0], max(parts, key=lambda x: x[0])[0] + 1):
			col = [part for part in parts if part[0] == i]
			down.append(min(col, key=lambda x: x[1]))
		return left, right, down
	
	@property
	def height(self):
		return self.y + self.l[1]
	
	def update_pos(self, cur_height):
		self.x, self.y = 2, cur_height - self.s[1] + 4

	def move_right(self, pile):
		if (self.x + self.max_x + 1) == 7: return False
		for delta_x, delta_y in self.right:
			if pile.get_entry(self.x + delta_x + 1, self.y + delta_y) != '.': return False
		return True

	def move_left(self, pile):
		if (self.x + self.min_x - 1) == -1: return False
		for delta_x, delta_y in self.left:
			if pile.get_entry(self.x + delta_x - 1, self.y + delta_y) != '.': return False
		return True
	
	def move_down(self, pile):
		if (self.y + self.min_y - 1) == -1: return False
		for delta_x, delta_y in self.down:
			if pile.get_entry(self.x + delta_x, self.y + delta_y - 1) == '#': return False 
		return True

	def push_rock(self, pile, ins):
		if ins == '>':
			self.x += 1 if self.move_right(pile) else 0
		else:
			self.x += -1 if self.move_left(pile) else 0


def construct_rocks():
	rocks = []
	rocks.append(Rock([(0, 0), (1, 0), (2, 0), (3, 0)]))
	rocks.append(Rock([(0, 0), (1, 1), (1, -1), (2, 0), (1, 0)]))
	rocks.append(Rock([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]))
	rocks.append(Rock([(0, 0), (0, 1), (0, 2), (0, 3)]))
	rocks.append(Rock([(0, 0), (0, 1), (1, 0), (1, 1)]))
	return rocks


def simulate(instructions, rounds):
	rocks = construct_rocks()
	pile = Pile(rounds)
	n, m = len(rocks), len(instructions)
	i, j = 0, 0
	rock = rocks[i]
	count = 0
	while count != rounds:
		while True:
			ins = instructions[j % m]
			rock.push_rock(pile, ins)
			j += 1
			if not rock.move_down(pile):break
			rock.y -= 1

		pile.draw(rock)
		pile.height = rock.height if rock.height > pile.height else pile.height

		i = (i+1) % n
		count += 1
		rock = rocks[i]
		rock.update_pos(pile.height)
	return pile.height + 1 




if __name__ == '__main__':
	instructions = get_data(day=17, year=2022).strip()
	print("Part 1: ", simulate(instructions, 2022)) # 3168
	print("Part 2:", ((1000000000000-1706)//1700)*2642 + 2659 + 305) # 1554117647070

# part 2
# not feasible to simulate
# there was a pattern after the first cycle of instructions
# the first cycle required 1706 steps and increased the height by 2659
# each cycle after the first cycle required 1700 steps and increased the height by 2642
# there was a remainder of 194 rocks after all the complete cycles, which increased the height by 305
# the result could therefore be calculated manually as shown above