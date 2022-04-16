from collections import defaultdict
import operator
import math


def parse_input():
    found_template = False
    pairs = defaultdict(lambda: 0)
    counter = defaultdict(lambda: 0)
    rules = dict()
    with open("input.txt", 'r') as raw:
        for line in raw:
            if found_template:
                temp = line.strip().split(" -> ")
                rules[temp[0]] = temp[1]
            else:
                if line == '\n':
                    found_template = True
                else:
                    chars = line.strip()
                    for i in range(len(chars))[1::]:
                        pairs[chars[i-1] + chars[i]] += 1
                        counter[chars[i-1]] += 1
                    counter[chars[len(chars)-1]] += 1

    return pairs, rules, counter


def main():
    pairs, rules, counter = parse_input()
    depth = 40
    for current_depth in range(depth):
        new_pairs = defaultdict(lambda: 0)
        for key in pairs.keys():
            new_char = rules[key]
            new_pairs[new_char + key[1]] += pairs[key]
            new_pairs[key[0] + new_char] += pairs[key]
            counter[new_char] += pairs[key]
        pairs = new_pairs

    # Most common element count minus least common element count.
    print(max(counter.values()) - min(counter.values()))


if __name__ == "__main__":
    main()