from itertools import product
import math


# Converts a base 10 number to a base 2(binary) number.
def converter(temp):
    number = int(temp)
    value = ''
    while number > 0:
        value += f"{number % 2}"
        number = math.floor(number / 2)
    return value


def combination(index, current_mask):
    value = converter(index)
    value = value[::-1].zfill(36)[::-1]
    result = ''
    memory_addresses = []
    indexes = []
    second_base = []
    for i, mask in enumerate(current_mask[::-1]):
        if mask == '0':
            result += value[i]
        elif mask == '1':
            result += '1'
        else:
            result += 'X'
            second_base.append([0, 1])
            indexes.append(i)
    combs = list(product(*second_base))
    for comb in combs:
        result_n = list(result)
        for i, c in enumerate(comb):
            result_n[indexes[i]] = c
        memory_addresses.append(''.join(map(str, result_n))[::-1])
    return memory_addresses


def main():
    mem = {}
    with open('input.txt', 'r') as raw:
        for line in raw:
            temp = line.strip().split()
            if temp[0] == 'mask':
                current_mask = temp[2]
            elif 'mem' in temp[0]:
                index = int("".join(i for i in temp[0] if i.isdigit()))
                for comb in combination(index, current_mask):
                    mem[comb] = int(temp[2])
    total_value = 0
    for value in mem.values():
        total_value += value
    print(f"The sum of all values left in memory is: {total_value}.")


if __name__ == "__main__":
    main()
