def acc(instruction, value):
    instruction[3] += 1
    if instruction[3] > 1:
        return False, value
    if instruction[2] == '+':
        return True, value + int(instruction[1])
    else:
        return True, value - int(instruction[1])


def jmp(instruction, index):
    instruction[3] += 1
    if instruction[3] > 1:
        return False, index
    if instruction[2] == '+':
        return True, index + int(instruction[1])
    else:
        return True, index - int(instruction[1])


def get_accumulators_count(instructions, index):
    value = 0
    running = True
    try:
        if instructions[index][0] == 'acc':
            running, value = acc(instructions[index], value)
        elif instructions[index][0] == 'jmp':
            running, index = jmp(instructions[index], index)
            if running is True:
                return get_accumulators_count(instructions, index)
            else:
                return value
    except:
        print("The code was successfully executed!")
        return value
    if running is True:
        return value + get_accumulators_count(instructions, index + 1)
    else:
        return value


def main():
    instructions = []
    with open('input.txt', 'r') as raw_data:
        for raw_instruction in raw_data:
            temp = raw_instruction.strip().split()
            symbol = temp[1][0]
            temp[1] = temp[1][1:]
            temp.append(symbol)
            # Adding extra element in list to register how many times a instruction is visited.
            temp.append(0)
            instructions.append(temp)

    value = get_accumulators_count(instructions, 0)
    print(f"The value of the accumulator is: {value}.")


if __name__ == "__main__":
    main()
