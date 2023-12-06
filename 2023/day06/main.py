from sympy import symbols, solve
import math

def part_1(times, distances):
    """Find the number of ways to win in each race and then multiply them together"""
    answer = 1
    for time, distance in zip(times, distances):
        t = symbols('t')
        equation = t * (time - t) - distance
        solutions = solve(equation, t)
        t_1, t_2 = math.ceil(solutions[0]), math.floor(solutions[1])
        answer *= (t_2 - t_1 + 1)
    return answer

def part_2(times, distances):
    """Finds the number of ways to win in the new single race"""
    time  = [int("".join(map(str, times)))] 
    distance = [int("".join(map(str, distances)))]
    return part_1(time, distance)


def main():
    times = [44, 89, 96, 91]
    distances = [277, 1136, 1890, 1768]
    print("Part 1: ", part_1(times, distances)) # 2344708
    print("Part 2: ", part_2(times, distances)) # 30125202


if __name__ == "__main__":
    main()
