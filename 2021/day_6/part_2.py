import heapq
import math


def parse_input():
    with open("input.txt", 'r') as raw:
        result = [[int(char) for char in line.strip()] for line in raw]
    return result


# A* algorithm, finding the shortest path using min heap.
def a_star(maze):
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]
    min_heap = [(0, 0, 0)]
    paths = [[None for _ in range(len(maze[i]))]for i in range(len(maze))]
    rows = len(maze)
    cols = len(maze[0])

    while len(min_heap) != 0:

        # Popping the root node of the heap(minimum value).
        (dist, x, y) = heapq.heappop(min_heap)

        # Skips if the position is out of range.
        if (x < 0) or (x >= rows) or (y < 0) or (y >= cols):
            continue

        # New heuristic
        re_cost = dist + maze[x][y]

        # Position is not visited or the heuristic is less than the current.
        if (paths[x][y] is None) or (re_cost < paths[x][y]):
            # The better heuristic is chosen
            paths[x][y] = re_cost
        else:
            continue
# Found the goal.
        if (x == rows - 1) and (y == cols - 1):
            # Returns heuristic minus the heuristic in the starting entry.
            return paths[x][y] - maze[0][0]
# Generating children.
        for i in range(4):
            child_x = x + DR[i]
            child_y = y + DC[i]
            heapq.heappush(min_heap, (paths[x][y], child_x, child_y))

    return "Not found"


def main():
    maze = parse_input()
    big_maze = []
    states = [0, 0]
    for row in range(5*len(maze)):
        big_maze.append([])
        states[0] = math.floor(row/len(maze))
        for col in range(5*len(maze[0])):
            states[1] = math.floor(col/len(maze[0]))
            if maze[row-len(maze)*states[0]][col-len(maze[0])*states[1]] + states[0] + states[1] > 9:
                entry = (maze[row-len(maze)*states[0]][col-len(maze[0])*states[1]] + states[0] + states[1] + 1) % 10
            else:
                entry = (maze[row - len(maze) * states[0]][col - len(maze[0]) * states[1]] + states[0] + states[1]) % 10
            big_maze[row].append(entry)

    print(a_star(maze))
    print(a_star(big_maze))


if __name__ == "__main__":
    main()