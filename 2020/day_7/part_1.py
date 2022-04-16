
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
        temp_queue = []
        running = True
        quitting = False
        # Here im using while loop because i dont know how many bags are inside the bags and so on...
        # Im using BFS(breath-first search algorithm) to find the possible shortest path to the shiny gold bag.
        while running:
            if len(queue) == 0:
                running = False
            for bag in queue:
                if quitting:
                    break
                else:
                    new_queue = luggage_data[bag[1]]
                    for bag_ in new_queue:
                        if 'shiny gold' in bag_[1]:
                            count += 1
                            running = False
                            quitting = True
                            break
                        else:
                            temp_queue.append(bag_)
            queue = temp_queue
            temp_queue = []
    print(f"The number of bags containing at least one shiny gold is: {count}")


if __name__ == "__main__":
    main()
