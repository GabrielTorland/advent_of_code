from collections import defaultdict

def parse(ans):
    with open("input.txt", 'r') as raw:
        diff = defaultdict(lambda: list())
        numbers = [int(number.strip()) for number in raw.readlines()]
        for i in range(len(numbers)):
            for j in range(len(numbers)):
                if i != j:        
                    diff[ans-numbers[i]-numbers[j]] = [numbers[i], numbers[j]]
    return diff, numbers

def part_2():    
    diff, numbers = parse(2020)
    for number in numbers:
        if len(diff[number]) != 0:
            return number*diff[number][0]*diff[number][1]

print(part_2())

