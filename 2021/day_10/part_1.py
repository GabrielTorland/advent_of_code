from collections import defaultdict


def parse_text():
    with open("input.txt", 'r') as raw:
        result = [line.strip() for line in raw]
    return result


def main():
    data = parse_text()
    next_char = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    errors = defaultdict(lambda: 0)

    for line in data:
        stack = list()
        for char in line:
            if char in next_char.keys():
                stack.append(next_char[char])
            else:
                if char == stack[-1]:
                    stack.pop()
                else:
                    errors[char] += 1
                    stack.pop()

    print(errors[')']*3+errors[']']*57+errors['}']*1197+errors['>']*25137)


if __name__ == "__main__":
    main()
