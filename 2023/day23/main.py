from collections import deque

class Maze:
    def __init__(self, maze_raw):
        self.maze_raw = maze_raw
        self.maze_nr_rows = len(maze_raw)
        self.maze_nr_cols = len(maze_raw[0])
        self.start_pos = (0, maze_raw[0].index('.'))
        self.stop_pos = (self.maze_nr_rows - 1, self.maze_raw[-1].index('.'))

    def get_possible_moves(self):
        raise NotImplementedError("Subclass must implement abstract method")


class MazeP1(Maze):
    def get_possible_moves(self, x, y):
        match self.maze_raw[x][y]:
            case '>':
                return [(x, y+1)]
            case '<':
                return [(x, y-1)]
            case '^':
                return [(x-1, y)]
            case 'v':
                return [(x+1, y)]
            case '.':
                neighbors = [(x, y+1), (x, y-1), (x-1, y), (x+1, y)]
                x_in_range = 0 <= x < self.maze_nr_rows
                y_in_range = 0 <= y < self.maze_nr_cols
                return [(x_c, y_c) for x_c, y_c in neighbors if x_in_range and y_in_range and self.maze_raw[x_c][y_c] != '#']
            
class MazeP2(Maze):
    def get_possible_moves(self, x, y):
        neighbors = [(x, y+1), (x, y-1), (x-1, y), (x+1, y)]
        x_in_range = 0 <= x < self.maze_nr_rows
        y_in_range = 0 <= y < self.maze_nr_cols
        return [(x_c, y_c) for x_c, y_c in neighbors if x_in_range and y_in_range and self.maze_raw[x_c][y_c] != '#']

class Path:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost
        self.visited = set()
    
    def __repr__(self) -> str:
        return f'Path(x={self.x}, y={self.y}, cost={self.cost})'

def parse(input_path='input.txt'):
    return [[char for char in line] for line in open(input_path).read().splitlines()]

def bfs(maze):
    queue = deque([Path(*maze.start_pos, 0)])
    solutions = []
    while queue: 
        path = queue.popleft()
        if (path.x, path.y) == maze.stop_pos:
            path.visited.add((path.x, path.y))
            solutions.append(path)
            continue
        possible_moves = maze.get_possible_moves(path.x, path.y)
        for possible_move in possible_moves:
            if possible_move in path.visited:
                continue
            child_path = Path(*possible_move, path.cost + 1)
            child_path.visited = path.visited.copy()
            child_path.visited.add((path.x, path.y))
            queue.append(child_path)
    return solutions

if __name__ == '__main__':
    maze_raw = parse()
    maze_p1 = MazeP1(maze_raw)
    print("Part 1: ", max(bfs(maze_p1), key=lambda x: x.cost).cost) # 1930
    maze_p2 = MazeP2(maze_raw)
    print("Part 2: ", max(bfs(maze_p2), key=lambda x: x.cost).cost) #