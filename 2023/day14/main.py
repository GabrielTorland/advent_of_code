import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift

def parse_input(input_path):
    stone_map = []
    with open(input_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        stone_map.append(np.array([x for x in line.strip()]))
    return np.array(stone_map) 

def push_north(stone_map, i, j):
    delta_i = 0
    while i-delta_i-1 >= 0 and stone_map[i-delta_i-1][j] not in ['#', 'O']:
        stone_map[i-delta_i][j], stone_map[i-delta_i-1][j] = stone_map[i-delta_i-1][j], stone_map[i-delta_i][j]
        delta_i += 1

def push_south(stone_map, i, j):
    delta_i = 0
    while i+delta_i+1 < len(stone_map) and stone_map[i+delta_i+1][j] not in ['#', 'O']:
        stone_map[i+delta_i][j], stone_map[i+delta_i+1][j] = stone_map[i+delta_i+1][j], stone_map[i+delta_i][j]
        delta_i += 1

def push_east(stone_map, i, j):
    delta_j = 0
    while j+delta_j+1 < len(stone_map[i]) and stone_map[i][j+delta_j+1] not in ['#', 'O']:
        stone_map[i][j+delta_j], stone_map[i][j+delta_j+1] = stone_map[i][j+delta_j+1], stone_map[i][j+delta_j]
        delta_j += 1

def push_west(stone_map, i, j):
    delta_j = 0
    while j-delta_j-1 >= 0 and stone_map[i][j-delta_j-1] not in ['#', 'O']:
        stone_map[i][j-delta_j], stone_map[i][j-delta_j-1] = stone_map[i][j-delta_j-1], stone_map[i][j-delta_j]
        delta_j += 1

def move_stones(stone_map_shape, direction):
    coordinates = []
    for i in range(stone_map_shape[0]):
        for j in range(stone_map_shape[1]):
            coordinates.append((i, j))
    match direction:
        case 'north':
            return push_north, coordinates
        case 'south':
            coordinates.sort(key=lambda x: x[0], reverse=True)
            return push_south, coordinates
        case 'east':
            coordinates.sort(key=lambda x: x[1], reverse=True)
            return push_east, coordinates
        case 'west':
            coordinates.sort(key=lambda x: x[1])
            return push_west, coordinates
        case _:
            raise ValueError("Invalid direction")

def push_plate(stone_map, direction): 
    stone_go, coordinates = move_stones(stone_map.shape, direction)
    for i, j in coordinates:
        # If ground or not movable stone, skip
        if stone_map[i][j] in ['.', '#']: continue
        stone_go(stone_map, i, j)

def calculate_total_load(stone_map):
    n = len(stone_map)
    return sum((n-i)*np.count_nonzero(stone_map[i] == 'O') for i in range(n))

def part_1(stone_map):
    push_plate(stone_map, 'north')
    return calculate_total_load(stone_map)

def plot_total_load_over_time(stone_map, rounds):
    total_load_history = []
    for _ in range(rounds):
        push_plate(stone_map, 'north')
        push_plate(stone_map, 'west')
        push_plate(stone_map, 'south')
        push_plate(stone_map, 'east')
        total_load_history.append(calculate_total_load(stone_map))

    plt.figure(figsize=(10, 6))
    plt.plot(total_load_history[80:100])
    plt.title("Total Load Over Time")
    plt.xlabel("Round")
    plt.ylabel("Total Load")
    plt.grid(True)
    plt.savefig('total_load_over_time.png')


def part_2(stone_map, target_rounds=1000000000):
    #plot_total_load_over_time(stone_map, 150)
    # It appears to converge to a specific sinusoidal like pattern
    # with a period of 17
    period = 17
    load_history = []
    for _ in range(period*2+1):
        push_plate(stone_map, 'north')
        push_plate(stone_map, 'west')
        push_plate(stone_map, 'south')
        push_plate(stone_map, 'east')
        load_history.append(calculate_total_load(stone_map))
    while not all(load_history[-period-1-i] == load_history[-1-i] for i in range(period)):
        push_plate(stone_map, 'north')
        push_plate(stone_map, 'west')
        push_plate(stone_map, 'south')
        push_plate(stone_map, 'east')
        load_history.append(calculate_total_load(stone_map))
    return load_history[((target_rounds - len(load_history)) % period)-period-1]

def main():
    stone_map = parse_input('input.txt')
    print("Part 1: ", part_1(stone_map)) # 109098
    stone_map = parse_input('input.txt')
    print("Part 2: ", part_2(stone_map))

if __name__ == "__main__":
    main()