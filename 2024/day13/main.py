import re
import numpy as np

class Button:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost

class ClawMachine:
    def __init__(self, button_a, button_b, target_x, target_y):
        self.button_a = button_a
        self.button_b = button_b
        self.target_x = target_x
        self.target_y = target_y

def parse(input_file="input.txt"):
    with open(input_file, "r") as f:
        raw_data = f.read().split("\n\n")
    claw_machines = []
    for line in raw_data:
        # extract all numbers with re
        numbers = re.findall(r"\d+", line)
        if len(numbers) != 6:
            print("Invalid input")
        x_a, y_a, x_b, y_b, x_target, y_target = numbers
        button_a = Button(int(x_a), int(y_a), 3)
        button_b = Button(int(x_b), int(y_b), 1)
        claw_machine = ClawMachine(button_a, button_b, int(x_target), int(y_target))
        claw_machines.append(claw_machine)
    return claw_machines

def get_minimal_cost(claw_machine):
    matrix = np.array([
        [claw_machine.button_a.x, claw_machine.button_b.x, claw_machine.target_x],
        [claw_machine.button_a.y, claw_machine.button_b.y, claw_machine.target_y]], dtype=np.int64)

    # Reduced row echelon form
    solution = np.linalg.solve(matrix[:, :-1], matrix[:, -1])
    # Exclude non-integer solutions
    rounded_solution = np.rint(solution)
    diff = np.abs(solution - rounded_solution)
    if np.any(diff > 1e-3):
        return None
    # Round to the nearest integer
    n, m = int(rounded_solution[0]), int(rounded_solution[1])
    if n < 0 or m < 0:
        return None
    return n*claw_machine.button_a.cost + m*claw_machine.button_b.cost

def p1(claw_machines):
    total_cost = 0
    for claw_machine in claw_machines:
        cost = get_minimal_cost(claw_machine)
        if cost is None:
            continue
        total_cost += cost
    return total_cost

def p2(claw_machines):
    for claw_machine in claw_machines:
        claw_machine.target_x += 10000000000000
        claw_machine.target_y += 10000000000000

    total_cost = 0
    for claw_machine in claw_machines:
        cost = get_minimal_cost(claw_machine)
        if cost is None:
            continue
        total_cost += cost
    return total_cost

if __name__ == "__main__":
    claw_machines = parse()
    print("Part 1:", p1(claw_machines))
    print("Part 2:", p2(claw_machines))
