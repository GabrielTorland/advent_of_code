from aocd import get_data
import re
import sys
sys.set_int_max_str_digits(0)


class Monkey:
	def __init__(self, start, dest, divider, oper_str) -> None:
		self.queue = start
		self.inspections = 0
		self.dest = dest
		self.divider = divider
		self.oper_str = oper_str

	def enqueue(self, items):
		self.queue.extend(items)
	@property
	def size_of_queue(self):
		return len(self.queue)
	def inspect(self):
		if self.size_of_queue == 0:
			raise Exception("No items to inspect")
		else:
			worry_lvl = self.__dequeue()
			worry_lvl = self.__oper(worry_lvl)
			worry_lvl = self.__bored(worry_lvl)
			self.inspections += 1
			return self.__test(worry_lvl), worry_lvl 

	def __dequeue(self):
		return self.queue.pop(0)
	def __oper(self, worry_lvl):
		equation = self.oper_str.replace("old", str(worry_lvl))
		return eval(equation)
	def __bored(self, worry_lvl):
		return worry_lvl // 3
	def __test(self, worry_lvl):
		return self.dest[0] if worry_lvl % self.divider == 0 else self.dest[1]


def parse(data):
	monkeys = []
	for monkey in data:
		start = [int(match) for match in re.search(r"items: (\d+.*)*", monkey).group(1).split(", ")]
		oper_str = re.search(r"old [+*] (\d+|old)", monkey).group(0)
		test = int(re.search(r"divisible by (\d+)", monkey).group(1))
		dest = [int(re.search(r"true: throw to monkey (\d+)", monkey).group(1)), int(re.search(r"false: throw to monkey (\d+)", monkey).group(1))]
		monkeys.append(Monkey(start, dest, test, oper_str))
	return monkeys

def simulate_rounds(monkeys, n):
	for i in range(n):
		for monkey in monkeys:
			while monkey.size_of_queue > 0:
				dest, worry_lvl = monkey.inspect()
				monkeys[dest].enqueue([worry_lvl])
	return monkeys


if __name__ == '__main__':
	data = get_data(day=11, year=2022).split("\n\n")
	monkey = parse(data)
	monkeys = sorted(simulate_rounds(monkey, 20), key=lambda monkey: monkey.inspections, reverse=True)
	print("Part 1: ", monkeys[0].inspections * monkeys[1].inspections) # 107822
