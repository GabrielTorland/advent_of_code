
class Node:
    def __init__(self):
        self.value = None
        self.operators = []
        self.value_pack = False
        self.children = []
        self.parent = None

    def insert_value(self, value):
        self.value = value
        self.value_pack= True

    def add_operator(self, operator):
        self.operators.append(operator)

    def add_child_without_value(self):
        child = Node()
        self.children.append(child)
        child.parent = self
        child.value = "()"
        return child
    def add_child_with_value(self, value):
        child = Node()
        child.insert_value(value)
        self.children.append(child)
        child.parent = self
    
def parse():
    with open("input.txt") as f:
        equations = list()
        for line in f.readlines():
            root = Node()
            node = root
            for c in line.strip().replace(' ', ''):
                if c.isdigit():
                    node.add_child_with_value(int(c))
                elif c in ['+', '*']:
                    node.add_operator(c)
                elif c == '(':
                    node = node.add_child_without_value()
                elif c == ')':
                    node = node.parent
            equations.append(root)
    return equations

def solve_equation(equation, operator_index):
    i = operator_index
    values = []
    operator = ""
    for child in equation.children:
        if child.value_pack:
            values.append(child.value)
            if len(values) == 2:
                if operator == '+':
                    values = [values[0] + values[1]]
                elif operator == '*':
                    values = [values[0] * values[1]]
                i += 1
            if (i <= len(equation.operators) - 1):
                operator = equation.operators[i]
        else:
            values.append(solve_equation(child, 0))
            if len(values) == 2:
                if operator == '+':
                    values = [values[0] + values[1]]
                elif operator == '*':
                    values = [values[0] * values[1]]
                i += 1
            if (i <= len(equation.operators) - 1):
                operator = equation.operators[i]
    return values[0]
         
            
def part_1():
    equations = parse()
    ans = 0
    for equation in equations:
       ans += solve_equation(equation, 0)
    return ans
print(part_1())
