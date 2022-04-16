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
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    fixes = list()

    for line in data:
        stack = list()
        current_fixes = list()
        for char in line:
            if char in next_char.keys():
                stack.append(next_char[char])
            else:
                if char == stack[-1]:
                    stack.pop()
                else:
                    current_fixes.append(stack[-1])
                    stack.pop()
        if len(current_fixes) == 0:
            current_fixes += stack
            fixes.append(current_fixes[::-1])
    scores = list()
    for fix in fixes:
        score = 0
        for detail in fix:
            score = score*5 + points[detail]
        scores.append(score)
    scores.sort()
    print(scores[int((len(scores)-1)/2)])


if __name__ == "__main__":
    main()