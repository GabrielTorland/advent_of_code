import sys
import numpy as np
import re


def parse_data_file():
    """
    Parse the data file and return a numpy array of integers.

    Returns:
        numpy.ndarray: A numpy array containing integers read from the input file.
    """
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    with open(infile) as f:
        # Convert list to numpy array
        data = np.array([int(elem) for elem in f.read().strip().split(',')])
        return data


def main():
    data = parse_data_file()
    i = 0
    while True:
        instruction = str(data[i])

        # Sum operation
        if re.fullmatch(r"1", instruction):
            data[data[i+3]] = data[data[i+1]] + data[data[i+2]]
        # Multiplication operation
        elif re.fullmatch(r"2", instruction):
            data[data[i+3]] = data[data[i+1]] * data[data[i+2]]
        # User input operation
        elif re.fullmatch(r"3", instruction):
            data[data[i+1]] = int(input("Enter an instruction:  "))
            i -= 2
        # Print operation
        elif re.fullmatch(r"4", instruction):
            print(data[data[i+1]])
            i -= 2
        # Jump-if-true operation
        elif re.fullmatch(r"5", instruction):
            if data[data[i+1]] != 0:
                i = data[data[i+2]] - 4
            else:
                i -= 1
        # Jump-if-false operation
        elif re.fullmatch(r"6", instruction):
            if data[data[i+1]] == 0:
                i = data[data[i+2]] - 4
            else:
                i -= 1
        # Less-than operation
        elif re.fullmatch(r"7", instruction):
            if data[data[i+1]] < data[data[i+2]]:
                data[data[i+3]] = 1
            else:
                data[data[i+3]] = 0
        # Equals operation
        elif re.fullmatch(r"8", instruction):
            if data[data[i+1]] == data[data[i+2]]:
                data[data[i+3]] = 1
            else:
                data[data[i+3]] = 0
        # Terminate operation
        elif re.fullmatch(r"99$", instruction):
            break
        # Handling other operations with parameter modes
        else:
            # Extract parameter modes
            m1, m2 = [(data[i] // 10**n) % 10 for n in range(2, 4)]
            num1 = data[i+1] if m1 == 1 else data[data[i+1]]
            num2 = data[i+2] if m2 == 1 else data[data[i+2]]

            # Sum operation with parameter modes
            if re.fullmatch(r".*01$", instruction):
                data[data[i+3]] = num1 + num2
            # Multiplication operation with parameter modes
            elif re.fullmatch(r".*02$", instruction):
                data[data[i+3]] = num1 * num2
            # Print operation with parameter mode
            elif re.fullmatch(r".*04$", instruction):
                print(num1 if m1 == 1 else data[num1])
            # Jump-if-true operation with parameter modes
            elif re.fullmatch(r".*05$", instruction):
                if num1 != 0:
                    i = num2 - 4
                else:
                    i -= 1
            # Jump-if-false operation with parameter modes
            elif re.fullmatch(r".*06$", instruction):
                if num1 == 0:
                    i = num2 - 4
                else:
                    i -= 1
            # Less-than operation with parameter modes
            elif re.fullmatch(r".*07$", instruction):
                if num1 < num2:
                    data[data[i+3]] = 1
                else:
                    data[data[i+3]] = 0
            # Equals operation with parameter modes
            elif re.fullmatch(r".*08$", instruction):
                if num1 == num2:
                    data[data[i+3]] = 1
                else:
                    data[data[i+3]] = 0
            else:
                print("Error!")
        i += 4

if __name__ == "__main__":
    main()
               
