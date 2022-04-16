def recursion(queue, luggage_data):
    temp_queue = []
    count = 0
    for bag in queue:
        bags = luggage_data[bag[1]]
        for bag_ in bags:
            bag_ = (bag_[0] * bag[0], bag_[1])
            count += bag_[0]
            temp_queue.append(bag_)

    if len(temp_queue) == 0:
        return count
    else:
        return count + recursion(temp_queue, luggage_data)


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
    queue = [(1, 'shiny gold')]
    count += recursion(queue, luggage_data)
    print(f"A single shiny golden bag must contain {count} other bags.")


if __name__ == "__main__":
    main()
