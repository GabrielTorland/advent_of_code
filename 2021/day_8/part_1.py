

def parse_text():
    with open("input.txt", 'r') as raw:
        result = list()
        for line in raw:
            elements = line.strip().split(' ')
            result.append([(elements[:count:], elements[(count+1)::]) for count, element in enumerate(elements) if element == '|'])
    return result


def main():
    result = parse_text()
    lengths = [2, 4, 3, 7]
    print(sum([(sum([(1 if len(value) in lengths else 0) for value in element[0][1]])) for element in result]))


if __name__ == "__main__":
    main()