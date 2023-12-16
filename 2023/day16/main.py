import numpy as np
from collections import defaultdict
import sys

sys.setrecursionlimit(10000)

def parse_input(input_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()
    contraption = []
    for line in lines:
        contraption.append(np.array([char for char in line.strip()]))
    return np.array(contraption)

def simulate_light_interaction(contraption, direction_to_delta, i, j, direction, visited): 
    if (direction in visited[(i, j)]) or (i < 0) or (i >= contraption.shape[0]) or (j < 0) or (j >= contraption.shape[1]):
        return
    visited[(i, j)].add(direction)
    match contraption[i][j]:
        case '.':
            new_i, new_j = i + direction_to_delta[direction][0], j + direction_to_delta[direction][1]
            simulate_light_interaction(contraption, direction_to_delta, new_i, new_j, direction, visited)
        case '|':
            if direction in ['right', 'left']:
                simulate_light_interaction(contraption, direction_to_delta, i+1, j, 'down', visited)
                simulate_light_interaction(contraption, direction_to_delta, i-1, j, 'up', visited)
            else:
                new_i, new_j = i + direction_to_delta[direction][0], j + direction_to_delta[direction][1]
                simulate_light_interaction(contraption, direction_to_delta, new_i, new_j, direction, visited)
        case '-':
            if direction in ['up', 'down']:
                simulate_light_interaction(contraption, direction_to_delta, i, j+1, 'right', visited)
                simulate_light_interaction(contraption, direction_to_delta, i, j-1, 'left', visited)
            else:
                new_i, new_j = i + direction_to_delta[direction][0], j + direction_to_delta[direction][1]
                simulate_light_interaction(contraption, direction_to_delta, new_i, new_j, direction, visited)
        case '/':
            if direction == 'up':
                simulate_light_interaction(contraption, direction_to_delta, i, j+1, 'right', visited)
            elif direction == 'right':
                simulate_light_interaction(contraption, direction_to_delta, i-1, j, 'up', visited)
            elif direction == 'down':
                simulate_light_interaction(contraption, direction_to_delta, i, j-1, 'left', visited)
            else:
                simulate_light_interaction(contraption, direction_to_delta, i+1, j, 'down', visited)
        case '\\':
            if direction == 'up':
                simulate_light_interaction(contraption, direction_to_delta, i, j-1, 'left', visited)
            elif direction == 'right':
                simulate_light_interaction(contraption, direction_to_delta, i+1, j, 'down', visited)
            elif direction == 'down':
                simulate_light_interaction(contraption, direction_to_delta, i, j+1, 'right', visited)
            else:
                simulate_light_interaction(contraption, direction_to_delta, i-1, j, 'up', visited) 

def part_1(contraption, i=0, j=0, direction='right'):
    direction_to_delta = {
        'right': (0,1),
        'left': (0,-1),
        'up': (-1,0),
        'down': (1,0)
    }
    visited = defaultdict(set)  
    simulate_light_interaction(contraption, direction_to_delta, i, j, direction, visited)
    return {position for position, directions in visited.items() if len(directions) > 0}

def part_2(contraption):
    max_num_energized = 0
    # top
    for i in range(contraption.shape[1]):
        max_num_energized = max(max_num_energized, len(part_1(contraption, 0, i, 'down')))
    # bottom
    for i in range(contraption.shape[1]):
        max_num_energized = max(max_num_energized, len(part_1(contraption, contraption.shape[0], i, 'up')))
    # left
    for i in range(contraption.shape[0]):
        max_num_energized = max(max_num_energized, len(part_1(contraption, i, 0, 'right')))
    # right
    for i in range(contraption.shape[0]):
        max_num_energized = max(max_num_energized, len(part_1(contraption, i, contraption.shape[1], 'left')))

    return max_num_energized 
        
def main():
    contraption = parse_input('input.txt')
    print("Part 1: ", len(part_1(contraption))) # 8112
    print("Part 2: ", part_2(contraption)) # 8314


if __name__ == '__main__':
    main()