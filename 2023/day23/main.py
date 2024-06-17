from collections import deque, defaultdict
from functools import lru_cache

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
    @lru_cache
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
                x_in_range = lambda x: 0 <= x < self.maze_nr_rows
                y_in_range = lambda y: 0 <= y < self.maze_nr_cols
                return [(x_c, y_c) for x_c, y_c in neighbors if x_in_range(x_c) and y_in_range(y_c) and self.maze_raw[x_c][y_c] != '#']

class MazeP2(Maze):
    @lru_cache
    def get_possible_moves(self, x, y):
        neighbors = [(x, y+1), (x, y-1), (x-1, y), (x+1, y)]
        x_in_range = lambda x: 0 <= x < self.maze_nr_rows
        y_in_range = lambda y: 0 <= y < self.maze_nr_cols
        return [(x_c, y_c) for x_c, y_c in neighbors if x_in_range(x_c) and y_in_range(y_c) and self.maze_raw[x_c][y_c] != '#']

class Node:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost
        self.neighbors = set()
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


def create_contracted_graph(maze_raw):
    maze_nr_rows = len(maze_raw)
    start_pos = (0, maze_raw[0].index('.'))
    queue = deque([start_pos])
    # Helper function to get possible moves
    def get_possible_moves(maze_raw, x, y):
        neighbors = [(x, y+1), (x, y-1), (x-1, y), (x+1, y)]
        x_in_range = lambda x: 0 <= x < maze_nr_rows
        y_in_range = lambda y: 0 <= y < len(maze_raw[0])
        return [(x_c, y_c) for x_c, y_c in neighbors if x_in_range(x_c) and y_in_range(y_c) and maze_raw[x_c][y_c] != '#']
    graph = defaultdict(list)
    visited = set()
    # Create the initial graph with nodes for each possible position in the maze
    while queue:
        x, y = queue.popleft()
        possible_moves = get_possible_moves(maze_raw, x, y) 
        for possible_move in possible_moves:
            graph[(x, y)].append((possible_move, 1))
            if possible_move in visited:
                continue
            queue.append(possible_move)
        visited.add((x, y)) 
    print("Original size: ", len(graph))
    
    # Contract the graph by removing nodes with only 2 neighbors
    # Keep track of the cost of the path between the neighbors
    not_satisfied = [node for node, neighbors in graph.items() if len(neighbors) == 2]
    while len(not_satisfied) > 0:
        node = not_satisfied[0] 
        neighbors = graph[node]
        graph[neighbors[0][0]].append((neighbors[1][0], neighbors[1][1] + neighbors[0][1]))
        graph[neighbors[0][0]] = [neighbor for neighbor in graph[neighbors[0][0]] if neighbor[0] != node]
        graph[neighbors[1][0]].append((neighbors[0][0], neighbors[0][1] + neighbors[1][1]))
        graph[neighbors[1][0]] = [neighbor for neighbor in graph[neighbors[1][0]] if neighbor[0] != node]
        del graph[node]
        not_satisfied = [node for node, neighbors in graph.items() if len(neighbors) == 2]
    print("Contracted size: ", len(graph))
    return graph
        
def bfs_graph(graph, start_pos, stop_pos):
    queue = deque([Path(*start_pos, 0)])
    solutions = []
    while queue: 
        path = queue.popleft()
        if (path.x, path.y) == stop_pos:
            path.visited.add((path.x, path.y))
            solutions.append(path)
            continue
        possible_moves = graph[(path.x, path.y)]
        for possible_move, cost in possible_moves:
            if possible_move in path.visited:
                continue
            child_path = Path(*possible_move, path.cost + cost)
            child_path.visited = path.visited.copy()
            child_path.visited.add((path.x, path.y))
            queue.append(child_path)
    return solutions

if __name__ == '__main__':
    maze_raw = parse()
    maze_p1 = MazeP1(maze_raw)
    print("Part 1: ", max(bfs(maze_p1), key=lambda x: x.cost).cost) # 1930
    graph = create_contracted_graph(maze_raw)
    print("Part 2: ", max(bfs_graph(graph, (0, maze_raw[0].index('.')), (len(maze_raw) - 1, maze_raw[-1].index('.'))), key=lambda x: x.cost).cost) # 1930