def acc(instruction, value):
    instruction[3] += 1
    if instruction[3] > 1:
        return False, value
    if instruction[2] == '+':
        return True, value + int(instruction[1])
    else:
        return True, value - int(instruction[1])


def jmp(instruction):
    instruction[3] += 1
    if instruction[3] > 1:
        return False, instruction[4]
    if instruction[2] == '+':
        return True, instruction[4] + int(instruction[1])
    else:
        return True, instruction[4] - int(instruction[1])


# TODO: The problem with this recursion function is to return a state back, hence i have to loop trough unnecessary
#  code. I leave this problem to be solved in the future...
def get_accumulators_count(instructions, index):
    value = 0
    running = True
    try:
        if instructions[index][0] == 'acc':
            running, value = acc(instructions[index], value)
        elif instructions[index][0] == 'jmp':
            instructions[index].append(index)
            running, index = jmp(instructions[index])
            if running is True:
                return get_accumulators_count(instructions, index)
            else:
                return value
    except:
        running = False
        print("The program terminated normally!")
    if running is True:
        return value + get_accumulators_count(instructions, index + 1)
    else:
        return value


def main():
    instructions_ = []
    with open('input.txt', 'r') as raw_data:
        for raw_instruction in raw_data:
            temp = raw_instruction.strip().split()
            symbol = temp[1][0]
            temp[1] = temp[1][1:]
            temp.append(symbol)
            # Adding extra element in list to register how many times a instruction is visited.
            temp.append(0)
            instructions_.append(temp)

    original_instructions = instructions_
    instructions = instructions_.copy()
    visited_instructions = []
    value = 0
    running = True
    index = 0
    while running:
        if instructions[index][0] == 'acc':
            running, value = acc(instructions[index], value)
        elif instructions[index][0] == 'nop':
            instructions[index].append(index)
            # Adding extra element in list to register current value of accumulator.
            instructions[index].append(value)
            visited_instructions.append(instructions[index])
        else:
            instructions[index].append(index)
            # Adding extra element in list to register current value of accumulator.
            instructions[index].append(value)
            visited_instructions.append(instructions[index])
            running, index = jmp(instructions[index])
            continue
        index += 1

    state = True
    sorted_instructions_visited = sorted(visited_instructions, key=lambda x: x[4], reverse=True)
    for instruction in sorted_instructions_visited:
        instructions__ = original_instructions.copy()
        if instruction[0] == 'jmp':
            instruction[0] = 'nop'
        else:
            instruction[0] = 'jmp'
        value = instruction[5]
        index = instruction[4]
        running_ = True
        while running_:
            try:
                if instructions__[index][0] == 'acc':
                    running_, value = acc(instructions__[index], value)
                elif instructions__[index][0] == 'jmp':
                    instructions__[index].append(index)
                    running_, index = jmp(instructions__[index])
                    continue
                index += 1
            except:
                running_ = False
                state = False
                print("The program terminated normally!")
                print(f"The value of the accumulator is: {value}.")
        if not state:
            break


if __name__ == "__main__":
    main()
