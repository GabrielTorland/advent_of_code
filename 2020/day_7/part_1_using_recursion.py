def recursion(queue, luggage_data):
    temp_queue = []
    for bag in queue:
        new_queue = luggage_data[bag[1]]
        for bag_ in new_queue:
            if 'shiny gold' in bag_[1]:
                return 1
            else:
                temp_queue.append(bag_)

    if len(temp_queue) == 0:
        return 0
    else:
        return recursion(temp_queue, luggage_data)


def main():
    luggage_data = {}
    with open('input.txt', 'r') as raw_data:
        for line in raw_data:
            temp = line.strip()
            words = temp.split()
            key = ""
            value_color = ""
            values = []
            value = False

            # Here im storing the content of the bags in a dictionary as a tuple with count and color.
            for index, word in enumerate(words):
                if 'bag' in word and value is True:
                    value = False
                    values.append((count, value_color.strip()))
                    value_color = ""
                elif value:
                    value_color += " " + word

                if index <= 1:
                    key += " " + word
                elif word.isnumeric():
                    count = int(word)
                    value = True

            luggage_data[key.strip()] = values

    count = 0
    # Here im checking the first layer of bags to get a starting queue.
    for key in luggage_data:
        queue = [(1, key)]
        count += recursion(queue, luggage_data)
    print(f"The number of bags containing at least one shiny gold is: {count}")


if __name__ == "__main__":
    main()
