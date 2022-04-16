import itertools


def main():
    numbers_ = []
    with open('input.txt', 'r') as raw:
        for line in raw:
            temp = line.rstrip()
            numbers_.append(int(temp))

    for index, num in enumerate(numbers_[25:]):
        preamble_list = numbers_[index:index + 25]
        current_target = num
        combinations = []
        for num_ in itertools.combinations(preamble_list, 2):
            combinations.append(sum(num_))
        if current_target not in combinations:
            print(f"The first number without this property is: {num}.")
            break


if __name__ == "__main__":
    main()