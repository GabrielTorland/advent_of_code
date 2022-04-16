from collections import defaultdict
import math


def parse():
    with open("input.txt", 'r') as raw:
        numbers = defaultdict(lambda: 0)
        for line in raw:
            for num in line.strip().split(','):
                numbers[int(num)] += 1
    return numbers


def main():
    numbers = parse()
    least_fuel_position = math.inf
    for numb_1 in numbers.keys():
        temp_fuel_needed = 0
        for numb_2, count_2 in numbers.items():
            temp_fuel_needed += count_2*(abs(numb_2-numb_1))
        if temp_fuel_needed < least_fuel_position:
            least_fuel_position = temp_fuel_needed

    print(least_fuel_position)


if __name__ == "__main__":
    main()