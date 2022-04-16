from functools import lru_cache


@lru_cache
def direction(degree):
    if degree >= 0:
        if degree == 0:
            return 'E'
        elif degree == 90:
            return 'S'
        elif degree == 180:
            return 'W'
        elif degree == 270:
            return 'N'
        else:
            return direction(degree - 360)
    else:
        if degree == -270:
            return 'S'
        elif degree == -180:
            return 'W'
        elif degree == -90:
            return 'N'
        else:
            return direction(degree + 360)


def main():
    with open('input.txt', 'r') as raw:
        instructions = raw.read().splitlines()

    navigation_instructions = {'N': 0,
                               'S': 0,
                               'E': 0,
                               'W': 0,
                               'L': 0,
                               'R': 0,
                               }
    for instruction in instructions:
        if instruction[0] == 'F':
            navigation_instructions[direction(navigation_instructions['R'] - navigation_instructions['L'])] += \
                int(instruction[1:])
        else:
            navigation_instructions[instruction[0]] += int((instruction[1:]))
    print(
        f"The Manhattan distance is {abs(navigation_instructions['N'] - navigation_instructions['S']) + abs(navigation_instructions['E'] - navigation_instructions['W'])}.")


if __name__ == "__main__":
    main()
