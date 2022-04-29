import sys
import math

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    return [int(line.strip()) if i == 0 else [int(number) for number in line.replace(',x', '').split(',')] for i, line in enumerate(open(infile).readlines())]

def earliest_departure(data):
    delta = dict()
    for mod_ in data[1]:
        i = 0
        while True:
            if (data[0] + i) % mod_ == 0:
                delta[i] = mod_
                break
            i += 1
    return delta
result = earliest_departure(parse())
print(min(result.keys())*result[min(result.keys())])