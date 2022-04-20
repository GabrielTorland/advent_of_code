from collections import defaultdict

def parse(ans):
    with open("input.txt", 'r') as raw:
        diff = defaultdict(lambda: list())
        numbers = [int(number.strip()) for number in raw.readlines()]
        for i in range(len(numbers)):   
            diff[ans-numbers[i]] = [numbers[i]]
    return diff, numbers

def part_1():    
    diff, numbers = parse(2020)
    for number in numbers:
        if len(diff[number]) != 0:
            return number*diff[number][0]

print(part_1())