from aocd import get_data
import re

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
            self.operator_1 = int(self.__rest)
        else:
            # match an operator with regex
            self.operator = re.search(r"(\+|\-|\*|\/)", self.__rest).group(1)
            self.operand_1, self.operand_2 = self.__rest.split(f" {self.operator} ")


def parse(raw):
    monkeys = {}
    for line in raw.splitlines():
        monkey, rest = line.split(": ")
        monkeys[monkey] = Monkey(monkey, rest)
    for monkey in monkeys.values():
        monkey.parse_rest(monkeys)
    return monkeys

def sound_of_root(monkeys, current, computed):
    if not current.operator:
        return current.operator_1
    if current.name in computed.keys():
        return computed[current.name]
    if current.operator == "+":
        computed[current.name] = sound_of_root(monkeys, monkeys[current.operand_1], computed) + sound_of_root(monkeys, monkeys[current.operand_2], computed)
    elif current.operator == "-":
        computed[current.name] = sound_of_root(monkeys, monkeys[current.operand_1], computed) - sound_of_root(monkeys, monkeys[current.operand_2], computed)
    elif current.operator == "*":
        computed[current.name] = sound_of_root(monkeys, monkeys[current.operand_1], computed) * sound_of_root(monkeys, monkeys[current.operand_2], computed)
    else:
        computed[current.name] = sound_of_root(monkeys, monkeys[current.operand_1], computed) / sound_of_root(monkeys, monkeys[current.operand_2], computed)
    return computed[current.name]
    

if __name__ == '__main__':
    raw = get_data(day=21, year=2022)
    monkeys = parse(raw)
    print("Part 1: ", int(sound_of_root(monkeys, monkeys["root"], {}))) # 56490240862410
