import re

def parse(filename):
    """Splits the file into a list of rows."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

def part_1(lines):
    """Find the first and last numeric characters in each line and concatenates them."""
    numbers = []
    pattern = re.compile(r"\d")
    for line in lines:
        number = pattern.search(line).group(0) + pattern.search(line[::-1]).group(0)
        numbers.append(int(number))
    return numbers

def part_2(lines):
    """Find the first and last numeric characters/number spelled out in each line and concatenates them."""
    numbers = []
    # Dictionary to convert spelled out numbers to digits
    word_to_digit = {"one": '1', "two": '2', "three": '3', "four": '4', "five": '5', 
             "six": '6', "seven": '7', "eight": '8', "nine": '9'}
    # Pattern for to capture the first and last number spelled out 
    pattern_first = re.compile(r"(" + r"|".join(f"{key}|{value}" for key, value in word_to_digit.items()) + r")")
    pattern_last = re.compile(r"(" + r"|".join(f"{key[::-1]}|{value}" for key, value in word_to_digit.items()) + r")")
    for line in lines:
        # Find the first and last number, either spelled out or numeric
        first = pattern_first.search(line).group(0) 
        last = pattern_last.search(line[::-1]).group(0)[::-1] 
        # Concatenate the first and last number, converting to digits if necessary
        number = (first if first.isnumeric() else word_to_digit[first]) + (last if last.isnumeric() else word_to_digit[last])
        numbers.append(int(number))
    return numbers

def test_part_functions():
    """Tests the part_1 and part_2 functions on some examples."""
    lines = ["two1nine", "eightw2o3three", "abcone2threexyz", "xtwone3four",
             "4nineeightseven2", "zoneight234", "7pqrstsixteen"]

    expected_part_1 = [11, 23, 22, 33, 42, 24, 77]
    expected_part_2 = [29, 83, 13, 24, 42, 14, 76]

    actual_part_1 = []
    actual_part_2 = []

    for line in lines:
        actual_part_1 += part_1([line])
        actual_part_2 += part_2([line])

    assert actual_part_1 == expected_part_1
    assert actual_part_2 == expected_part_2

    print("All tests passed!")

def main():
    lines = parse('input.txt')
    test_part_functions()
    print("Part 1: ", sum(part_1(lines))) # 55712
    print("Part 2: ", sum(part_2(lines))) # 55413 

if __name__ == '__main__':
    main()