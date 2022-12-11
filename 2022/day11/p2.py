from aocd import get_data
import re
from functools import lru_cache

class WorryLvl:
	def __init__(self, prev, oper, worry_lvl) -> None:
		self.prev = prev
		self.__oper = oper
		self.worry_lvl = worry_lvl

	@lru_cache(maxsize=None)
	def value(self, divider):
		if self.prev is None:
			return self.worry_lvl
		elif self.__oper == '+':
			if isinstance(self.worry_lvl, int):
				return ((self.prev.value(divider) % divider) + (self.worry_lvl % divider)) % divider
			else:
				return (2*(self.prev.value(divider) % divider)) % divider
		else:
			if isinstance(self.worry_lvl, int):
				return ((self.prev.value(divider) % divider) * (self.worry_lvl % divider)) % divider
			else:
				return ((self.prev.value(divider) % divider)**2) % divider

class Item:
	def __init__(self, init) -> None:
		self.worry_lvl = WorryLvl(None, None, init)
	def oper(self, oper):
		if oper[0] == '+':
			self.worry_lvl = WorryLvl(self.worry_lvl, '+', int(oper[1]) if oper[1] != "old" else self.worry_lvl)
		else:
			self.worry_lvl = WorryLvl(self.worry_lvl, '*', int(oper[1]) if oper[1] != "old" else self.worry_lvl)
	def test(self, dest, divider):
		return dest[0] if self.worry_lvl.value(divider) == 0 else dest[1]

class Monkey:
	def __init__(self, start, dest, divider, oper) -> None:
		self.queue = [Item(item) for item in start]
		self.inspections = 0
		self.dest = dest
		self.oper = oper
		self.divider = divider

	def enqueue(self, item):
		self.queue.append(item)
	def __dequeue(self):
		return self.queue.pop(0)
	@property
	def size_of_queue(self):
		return len(self.queue)
	def inspect(self):
		if self.size_of_queue == 0:
			raise Exception("No items to inspect")
		else:
			worry_lvl = self.__dequeue()
			worry_lvl.oper(self.oper)
			self.inspections += 1
			return worry_lvl.test(self.dest, self.divider), worry_lvl

	
def parse(data):
	monkeys = []
	for monkey in data:
		start = [int(match) for match in re.search(r"items: (\d+.*)*", monkey).group(1).split(", ")]
		tmp = re.search(r"old ([+*]) (\d+|old)", monkey)
		oper = tmp.group(1), tmp.group(2)
		test = int(re.search(r"divisible by (\d+)", monkey).group(1))
		dest = [int(re.search(r"true: throw to monkey (\d+)", monkey).group(1)), int(re.search(r"false: throw to monkey (\d+)", monkey).group(1))]
		monkeys.append(Monkey(start, dest, test, oper))
	return monkeys

def simulate_rounds(monkeys, n):
	for _ in range(n):
		for monkey in monkeys:
			while monkey.size_of_queue > 0:
				dest, worry_lvl = monkey.inspect()
				monkeys[dest].enqueue(worry_lvl)
	return monkeys


if __name__ == '__main__':
	data = get_data(day=11, year=2022).split("\n\n")
	monkey = parse(data)
	monkeys = sorted(simulate_rounds(monkey, 10000), key=lambda monkey: monkey.inspections, reverse=True)
	print("Part 2: ", monkeys[0].inspections * monkeys[1].inspections) # 27267163742
