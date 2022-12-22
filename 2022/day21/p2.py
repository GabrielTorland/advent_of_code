from aocd import get_data
import re
from sympy import sympify, solveset
from sympy.parsing.sympy_parser import parse_expr

class Monkey:
	def __init__(self, name, rest):
		self.name = name
		self.__rest = rest
		self.operator = None
		self.operand_1 = None
		self.operand_2 = None

	def parse_rest(self, monkeys):
		# check if self.rest is a number
		if self.__rest.isdigit():
			self.operator_1 = int(self.__rest) if self.name != "humn" else "x"
		else:
			# match an operator with regex
			self.operator = re.search(r"(\+|\-|\*|\/)", self.__rest).group(1)
			self.operand_1, self.operand_2 = self.__rest.split(f" {self.operator} ")
			if self.operand_1 == "humn": self.operand_1 = "x"
			if self.operand_2 == "humn": self.operand_2 = "x"


def parse(raw):
	monkeys = {}
	for line in raw.splitlines():
		monkey, rest = line.split(": ")
		monkeys[monkey if monkey != "humn" else "x"] = Monkey(monkey, rest)
	for monkey in monkeys.values():
		monkey.parse_rest(monkeys)
	monkeys["root"].operator = "="
	return monkeys

def root_equality(monkeys, current, computed):
	if not current.operator:
		return current.operator_1
	if current.name in computed.keys():
		return computed[current.name]
	if current.operator == "+":
		computed[current.name] = f"({root_equality(monkeys, monkeys[current.operand_1], computed)} + {root_equality(monkeys, monkeys[current.operand_2], computed)})"
	elif current.operator == "-":
		computed[current.name] = f"({root_equality(monkeys, monkeys[current.operand_1], computed)} - {root_equality(monkeys, monkeys[current.operand_2], computed)})"
	elif current.operator == "*":
		computed[current.name] = f"({root_equality(monkeys, monkeys[current.operand_1], computed)} * {root_equality(monkeys, monkeys[current.operand_2], computed)})"
	elif current.operator == "/":
		computed[current.name] = f"({root_equality(monkeys, monkeys[current.operand_1], computed)} / {root_equality(monkeys, monkeys[current.operand_2], computed)})"
	else:
		computed[current.name] = f"{root_equality(monkeys, monkeys[current.operand_1], computed)} = {root_equality(monkeys, monkeys[current.operand_2], computed)}"
	return computed[current.name]
	

if __name__ == '__main__':
	raw = get_data(day=21, year=2022)
	monkeys = parse(raw)
	equation = root_equality(monkeys, monkeys["root"], {}).replace("=", "-")
	# solve the equation for x
	solution = solveset(parse_expr(equation), "x")
	print("Part 2: ", str(solution)[1:-1]) # 3403989691757
