import math


# Converts a a base 10 number to a base 2(binary) number.
def converter(temp):
    number = int(temp[2])
    value = ''
    while number > 0:
        value += f"{number % 2}"
        number = math.floor(number / 2)
    return value


def main():
    with open('input.txt', 'r') as raw:
        current_mask = None
        mem = {}
        for line in raw:
            temp = line.strip().split()
            if temp[0] == 'mask':
                current_mask = temp[2]
            elif 'mem' in temp[0]:
                value = converter(temp)
                value = value[::-1].zfill(36)[::-1]
                result = ""
                for index, bi in enumerate(current_mask[::-1]):
                    if bi == 'X':
                        result += value[index]
                    elif bi == '1':
                        result += '1'
                    else:
                        result += '0'
                result_ = [2 ** i for i in range(len(result)) if result[i] == '1']
                mem[int("".join(i for i in temp[0] if i.isdigit()))] = sum(result_)

        memory_sum = 0
        for val in mem.values():
            memory_sum += val
        print(f"The sum of all values left in memory is: {memory_sum}.")


if __name__ == "__main__":
    main()
