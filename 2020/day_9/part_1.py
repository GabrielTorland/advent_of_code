

def main():
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
                    temp = memo[num-num_1]
                    state = False
                    break
                except:
                    pass

        if state:
            print(f"The first number without this property is: {num}.")
            break


if __name__ == "__main__":
    main()
