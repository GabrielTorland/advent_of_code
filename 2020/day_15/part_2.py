def main():

    position = {12: [0], 1: [1], 16: [2], 3: [3], 11: [4], 0: [5]}
    starting_index = len(position)
    last_number_spoken = 0
    count = 30000000

    for i in range(count-starting_index):
        if len(position[last_number_spoken]) > 1:
            number = i+starting_index-1 - position[last_number_spoken][len(position[last_number_spoken])-2]
            last_number_spoken = number
            try:
                position[number].append(i+starting_index)
            except KeyError:
                position[number] = [i+starting_index]
        else:
            position[0].append(i+starting_index)
            last_number_spoken = 0

    print(f"The {count}th number spoken is: {last_number_spoken}.")


if __name__ == "__main__":
    main()
