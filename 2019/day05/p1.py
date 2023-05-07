import sys
import numpy as np
import re


def parse():
    """
    Parse the data file and return a list of lists of integers.
    """
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    with open(infile) as f:
        # Convert list to numpy array
        data = np.array([int(elem) for elem in f.read().strip().split(',')])
        return data

def main():
    data = parse()
    print(data[1])
    i = 0    
    while True:
        instruction = str(data[i])
        
        if re.fullmatch(r"1", instruction):
            data[data[i+3]] = data[data[i+1]] + data[data[i+2]]
        elif re.fullmatch(r"2", instruction):
            data[data[i+3]] = data[data[i+1]] * data[data[i+2]]
        elif re.fullmatch(r"3", instruction):
            data[data[i+1]] = int(input("Enter an instruction:  "))
            i -= 2
        elif re.fullmatch(r"4", instruction):
            print(data[data[i+1]])
            i -= 2
        elif re.fullmatch(r"99$", instruction):
            break
        elif re.fullmatch(r".*01$", instruction):
            num = data[i]
            m1, m2 = [(num // 10**n) % 10 for n in range(2, 4)]
            num1 = data[i+1] if m1 == 1 else data[data[i+1]]
            num2 = data[i+2] if m2 == 1 else data[data[i+2]]
            data[data[i+3]] = num1 + num2
        elif re.fullmatch(r".*02$", instruction):
            num = data[i]
            m1, m2 = ((num // 10**n) % 10 for n in range(2, 4))
            num1 = data[i+1] if m1 == 1 else data[data[i+1]]
            num2 = data[i+2] if m2 == 1 else data[data[i+2]]
            data[data[i+3]] = num1 * num2
        elif re.fullmatch(r".*04$", instruction):
            m1 = (data[i] // 10**2) % 10
            if m1 == 1:
                print(data[i+1]) 
            else:
                print(data[data[i+1]])
        else:
            print("Error!")
        i += 4

if __name__ == "__main__":
    main()