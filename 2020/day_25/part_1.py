import sys

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    return [int(key)for key in open(infile).readlines()]


def find_iterations(public_keys):
    iterations = list()
    for public_key in public_keys:
        current = 1
        i = 0
        while current != public_key:
            current = current*7 % 20201227
            i += 1
        iterations.append(i)
    return iterations

def find_encryption_keys(iterations, public_keys):
    encryption_keys = list()
    for i in range(2):
        current = 1
        for j in range(iterations[(i+1) % 2]):
            current = current*public_keys[i] % 20201227
        encryption_keys.append(current)
    return encryption_keys

public_keys = parse() 
print(find_encryption_keys(find_iterations(public_keys), public_keys))