
def oxygen_generator_rating(bit_strings):
    iterations = len(bit_strings[0])
    current = bit_strings
    for i in range(iterations):
        ones = set()
        zeros = set()
        for bit_string in current:
            if bit_string[i] == "1":
                ones.add(bit_string)
            else:
                zeros.add(bit_string)
        current = zeros if len(zeros) > len(ones) else ones
    return current.pop()


def CO2_scrubber_rating(bit_strings):
    iterations = len(bit_strings[0])
    current = bit_strings
    for i in range(iterations):
        ones = set()
        zeros = set()
        for bit_string in current:
            if bit_string[i] == "1":
                ones.add(bit_string)
            else:
                zeros.add(bit_string)
        if len(zeros) == 0:
            current = ones
        elif len(ones) == 0:
            current = zeros
        else:
            current = zeros if len(zeros) <= len(ones) else ones
    return current.pop()


def main():
    with open("input.txt", 'r') as raw:
        bit_strings = [line.strip() for line in raw]
    rating_1 = int(oxygen_generator_rating(bit_strings), 2)
    rating_2 = int(CO2_scrubber_rating(bit_strings), 2)
    print(f"The life support rating of the submarine is {rating_1*rating_2}")


if __name__ == "__main__":
    main()
