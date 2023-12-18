import numpy as np
from heapq import heappush, heappop

def parse_input(input_path='input.txt'):
    with open(input_path, 'r') as f:
        lines = f.readlines()
    return np.array([np.array([int(char) for char in line.strip()]) for line in lines])

def part_1(heat_map):
    queue = [(0, 0, 0, 0, 0, 0)]
    visited = set()
    while len(queue):
        current_heat_loss, x, y, dx, dy, n = heappop(queue)

        if (x, y, dx, dy, n) in visited:
            continue

        visited.add((x, y, dx, dy, n))

        if x == heat_map.shape[0]-1 and y == heat_map.shape[1]-1:
            return current_heat_loss

        if n < 3 and (dx, dy) != (0, 0):
            nx = x+dx
            ny = y+dy
            if 0 <= nx < heat_map.shape[0] and 0 <= ny < heat_map.shape[1]:
                heappush(queue, (current_heat_loss+heat_map[nx][ny], nx, ny, dx, dy, n+1))
        
        for new_dx, new_dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (new_dx, new_dy) == (dx, dy) or (new_dx, new_dy) == (-dx, -dy):
                continue
            nx = x+new_dx
            ny = y+new_dy
            if nx < 0 or nx >= heat_map.shape[0] or ny < 0 or ny >= heat_map.shape[1]:
                continue
            heappush(queue, (current_heat_loss+heat_map[nx][ny], nx, ny, new_dx, new_dy, 1))
    return None

def part_2(heat_map):
    queue = [(0, 0, 0, 0, 0, 0)]
    visited = set()
    while len(queue):
        current_heat_loss, x, y, dx, dy, n = heappop(queue)

        if (x, y, dx, dy, n) in visited:
            continue

        visited.add((x, y, dx, dy, n))

        if x == heat_map.shape[0]-1 and y == heat_map.shape[1]-1:
            return current_heat_loss

        if n < 10 and (dx, dy) != (0, 0):
            nx = x+dx
            ny = y+dy
            if 0 <= nx < heat_map.shape[0] and 0 <= ny < heat_map.shape[1]:
                heappush(queue, (current_heat_loss+heat_map[nx][ny], nx, ny, dx, dy, n+1))
        if n < 4 and not (dx, dy) == (0, 0):
            continue 
        for new_dx, new_dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (new_dx, new_dy) == (dx, dy) or (new_dx, new_dy) == (-dx, -dy):
                continue
            nx = x+new_dx
            ny = y+new_dy
            if nx < 0 or nx >= heat_map.shape[0] or ny < 0 or ny >= heat_map.shape[1]:
                continue
            heappush(queue, (current_heat_loss+heat_map[nx][ny], nx, ny, new_dx, new_dy, 1))
    return None

def main():
    heat_map = parse_input()
    print("Part 1: ", part_1(heat_map)) # 1246
    print("Part 2: ", part_2(heat_map)) # 1389

if __name__ == '__main__':
    main()