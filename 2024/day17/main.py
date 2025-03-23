import re
import math

def parse(input_file):
    raw_data = open(input_file).read()
    registers = {}
    registers["A"] = int(re.search(r"Register A: (\d+)", raw_data).group(1))
    registers["B"] = int(re.search(r"Register B: (\d+)", raw_data).group(1))
    registers["C"] = int(re.search(r"Register C: (\d+)", raw_data).group(1))

    program = []
    instructions = list(map(int, re.search(r"Program: ([\d,]+)", raw_data).group(1).split(',')))
    for i in range(0, len(instructions), 2):
        program.append((instructions[i], instructions[i+1]))
    return registers, program
def get_combo_operand(operand, registers):
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        return None

def run_program(registers, program):
    position = 0
    output = []
    while position < len(program):
        opcode, operand = program[position]
        jump = False
        match opcode:
            case 0:
                combo_operand = get_combo_operand(operand, registers)
                registers["A"] = math.trunc(registers["A"]/(2**combo_operand))
            case 1:
                registers["B"] = registers["B"] ^ operand
            case 2:
                combo_operand = get_combo_operand(operand, registers)
                registers["B"] = combo_operand % 8
            case 3:
                if registers["A"] != 0:
                    position = operand
                    jump = True
            case 4:
                registers["B"] = registers["B"] ^ registers["C"]
            case 5:
                combo_operand = get_combo_operand(operand, registers)
                value = combo_operand % 8
                output.append(value)
            case 6:
                combo_operand = get_combo_operand(operand, registers)
                registers["B"] = math.trunc(registers["A"]/(2**combo_operand))
            case 7:
                combo_operand = get_combo_operand(operand, registers)
                registers["C"] = math.trunc(registers["A"]/(2**combo_operand))
        if not jump:
            position += 1
    return ",".join(map(str, output))


def p1(registers, program):
    return run_program(registers, program)

def p2(registers, program):
    program_string = ",".join(map(lambda x: f"{x[0]},{x[1]}", program))
    found = False
    delta = 100000000000000
    increasing = True
    A = 0
    while not found:
        registers["A"] = A
        output = run_program(registers, program)
        if increasing == (len(output) < len(program_string)):
            print("Change in direction")
            print(f"Current A: {A}")
            print(f"Current delta: {delta}")
        if len(output) < len(program_string):
            A += delta
            if not increasing and not delta == 1:
                delta = delta // 10
            increasing = True
        else:
            A -= delta
            if increasing and not delta == 1:
                delta = delta // 10
            increasing = False
        if output == program_string:
            return A

if __name__ == "__main__":
    registers, program = parse("input.txt")
    print("Part 1:", p1(registers, program))
    print("Part 2:", p2(registers, program))