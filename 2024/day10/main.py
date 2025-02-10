def parse(input_file="input.txt"):
    with open(input_file, "r") as f:
        return [[int(height) for height in line] for line in f.read().splitlines()]

def get_start_positions(hike_map):
    start_positions = []
    for i, row in enumerate(hike_map):
        for j, height in enumerate(row):
            if height == 0:
                start_positions.append((i, j))
    return start_positions

def get_trail_heads(hike_map):
    trail_heads = []
    for i, row in enumerate(hike_map):
        for j, height in enumerate(row):
            if height == 9:
                trail_heads.append((i, j))
    return trail_heads

def bfs(hike_map, start_position):
    score = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = [start_position]
    visited = set(start_position)
    while queue:
        i, j = queue.pop(0)
        if hike_map[i][j] == 9:
            score += 1
            continue
        for direction in directions:
            new_i, new_j = i + direction[0], j + direction[1]
            if 0 <= new_i < len(hike_map) and 0 <= new_j < len(hike_map[0]) and (hike_map[new_i][new_j] - hike_map[i][j]) == 1  and (new_i, new_j) not in visited:
                visited.add((new_i, new_j))
                queue.append((new_i, new_j))
    return score

def bfs_no_visited(hike_map, trail_head):
    score = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = [trail_head]
    while queue:
        i, j = queue.pop(0)
        if hike_map[i][j] == 0:
            score += 1
            continue
        for direction in directions:
            new_i, new_j = i + direction[0], j + direction[1]
            if 0 <= new_i < len(hike_map) and 0 <= new_j < len(hike_map[0]) and (hike_map[new_i][new_j] - hike_map[i][j]) == -1:
                queue.append((new_i, new_j))
    return score

def p1(hike_map):
    start_positions = get_start_positions(hike_map)
    return sum([bfs(hike_map, start_position) for start_position in start_positions])

def p2(hike_map):
    trail_heads = get_trail_heads(hike_map)
    return sum([bfs_no_visited(hike_map, trail_head) for trail_head in trail_heads])

if __name__ == "__main__":
    hike_map = parse()
    print("Part 1:", p1(hike_map))
    print("Part 2:", p2(hike_map))