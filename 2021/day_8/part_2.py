from itertools import combinations
from collections import defaultdict
import copy


def parse_text():
    with open("input.txt", 'r') as raw:
        result = list()
        for line in raw:
            elements = line.strip().split(' ')
            result.append([(elements[:count:], elements[(count + 1)::]) for count, element in enumerate(elements) if
                           element == '|'])
    return result


def main():
    result = parse_text()
    patterns = [
        ({6: 3, 5: 3, 3: 1}, 'a'),  # [(6, 3), (5, 3), (3, 1), (7, 1)]
        ({6: 3, 5: 1, 4: 1}, 'b'),  # [(6, 3), (5, 1), (4, 1), (7, 1)]
        ({6: 2, 5: 2, 2: 1, 4: 1, 3: 1}, 'c'),  # [(6, 2), (5, 2), (2, 1), (4, 1), (3, 1), (7, 1)]
        ({6: 2, 5: 3, 4: 1}, 'd'),  # [(6, 2), (5, 3), (4, 1), (7, 1)]
        ({6: 2, 5: 1}, 'e'),  # [(6, 2), (5, 1), (7, 1)]
        ({6: 3, 2: 1, 5: 2, 4: 1, 3: 1}, 'f'),  # [(6, 3), (2, 1), (5, 2), (4, 1), (3, 1), (7, 1)]
        ({6: 3, 5: 3}, 'g')  # [(6, 3), (5, 3), (7, 1)]
    ]
    answer = list()
    for data in result:
        lengths = {
            2: set(),
            3: set(),
            4: set(),
            5: set(),
            6: set(),
            7: set()
        }
        alphabet = defaultdict(lambda: set())
        for code in data[0][0]:
            lengths[len(code)].add(code)
        for pattern in patterns:
            for comb_1 in list(combinations(list(lengths[5]), pattern[0][5])):
                for comb_2 in list(combinations(list(lengths[6]), pattern[0][6])):
                    new_code = set(lengths[7].copy().pop())
                    test = [set(val) for val in comb_1]
                    test += [set(val) for val in comb_2]
                    test += [set(list(lengths[key])[0]) for key in pattern[0].keys() if (key != 6 and key != 5)]
                    for code in test:
                        new_code = new_code.intersection(code)
                        if len(new_code) == 0:
                            break
                    if len(new_code) > 0:
                        for co in new_code:
                            alphabet[pattern[1]].add(co)

        secure = list()
        while len(secure) != len(alphabet):
            secure = [list(alphabet[key])[0] for key in alphabet.keys() if len(alphabet[key]) == 1]
            for key in alphabet.keys():
                if len(alphabet[key]) != 1:
                    for test in secure:
                        if test in alphabet[key]:
                            alphabet[key].remove(test)
        temp_answer = ""
        for value_ in data[0][1]:
            value = {value__ for value__ in value_}
            if len(value) == 2:
                temp_answer += '1'
            elif len(value) == 3:
                temp_answer += '7'
            elif len(value) == 4:
                temp_answer += '4'
            elif len(value) == 7:
                temp_answer += '8'
            elif len(value) == 5:
                if list(alphabet['c'])[0] not in value:
                    temp_answer += '5'
                elif list(alphabet['e'])[0] in value:
                    temp_answer += '2'
                else:
                    temp_answer += '3'
            elif len(value) == 6:
                if list(alphabet['d'])[0] not in value:
                    temp_answer += '0'
                elif list(alphabet['e'])[0] not in value:
                    temp_answer += '9'
                else:
                    temp_answer += '6'

        answer.append(int(temp_answer))
    print(sum(answer))


if __name__ == "__main__":
    main()