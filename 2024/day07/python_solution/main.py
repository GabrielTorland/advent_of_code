class Equation:
    def __init__(self, target, literals):
        self.target = target
        self.literals = literals

    def get_next(self, i):
        return self.literals[i]

    def is_last(self, i):
        return i == len(self.literals) - 1


def parse(input_file="input.txt"):
    with open(input_file, "r") as file:
        lines = file.readlines()
    equations = []
    for line in lines:
        target, numbers = line.split(": ")
        numbers = [int(number) for number in numbers.split(" ")]
        eq = Equation(int(target), numbers)
        equations.append(eq)
    return equations


def evaluate(eq, value, i, operators):
    next_number = eq.get_next(i)
    for next_value in [operator(value, next_number) for operator in operators]:
        if eq.is_last(i):
            if next_value == eq.target:
                return True
        elif next_value <= eq.target and evaluate(eq, next_value, i + 1, operators):
            return True
    return False


def part_(equations, operators):
    answer = 0
    for eq in equations:
        answer += eq.target if evaluate(eq, eq.get_next(0), 1, operators) else 0
    return answer


def concatenate(a, b):
    return int(str(a) + str(b))


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


if __name__ == "__main__":
    equations = parse()
    print("Part 1:", part_(equations, [add, multiply]))
    print("Part 2:", part_(equations, [add, multiply, concatenate]))

