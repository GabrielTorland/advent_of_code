import itertools


def target_1():
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
            return num


def target_2():
    numbers_ = []
    memo = {}
    with open('input.txt', 'r') as raw:
        for index, line in enumerate(raw):
            temp = line.rstrip()
            numbers_.append(int(temp))
            memo[int(temp)] = index

    for index, num in enumerate(numbers_[25:]):
        past_nums = numbers_[index:index + 25]
        past_nums.sort(reverse=True)
        state = True
        for num_1 in past_nums:
            if num_1 <= num:
                try:
                    temp = memo[num - num_1]
                    state = False
                    break
                except:
                    pass

        if state:
            return num


def main():
    numbers_ = []
    with open('input.txt', 'r') as raw:
        for line in raw:
            temp = line.rstrip()
            numbers_.append(int(temp))

    S = target_2()
    length = 3
    running = True
    while running:
        for i in range(len(numbers_)):
            preamble_list = numbers_[i:(i + length)]
            sum_preamble_list = sum(preamble_list)

            if sum_preamble_list == S:
                max_, min_ = max(preamble_list), min(preamble_list)
                print(
                    f"The encryption weakness was found! The sum of the smallest and the largest number is: "
                    f"{max_ + min_}.")
                running = False
                break

        length += 1


if __name__ == "__main__":
    main()
