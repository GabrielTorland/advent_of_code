import sys, heapq, copy
from dataclasses import dataclass, field
from typing import Any
import numpy as np
from collections import defaultdict, Counter

goals = {
    "A": [(2, 3), (3, 3), (4, 3), (5, 3)],
    "B": [(2, 5), (3, 5), (4, 5), (5, 5)],
    "C": [(2, 7), (3, 7), (4, 7), (5, 7)],
    "D": [(2, 9), (3, 9), (4, 9), (5, 9)],
    }
costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
    }
positions = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11)]
positions = positions+[point for val in goals.values() for point in val]

@dataclass(eq=True, init=True, order=True)
class Amphipod:
    type: str = field(compare=False, )
    x: int = field(compare=False)
    y: int = field(compare=False)
    maze: Any = field(compare=False)
    cost: int = field(compare=False)
    cur_cost: int
    cor_pos: int = field(compare=False, default=0)
    parent: 'Amphipod' = field(compare=False, default=None)
    
    def calc_moves(self):
        global goals, costs, positions
        
        goal = goals[self.type]
        x = self.x
        y_1 = self.y
        y_2 = self.y
        new_cur_cost = self.cur_cost
        children = []

        # Move up to hallway
        new_cur_cost += self.cost*(x-1)
        x = 1

        stop_right = False
        stop_left = False
        while not stop_left or not stop_right:
                    
            if self.maze[(x, y_1-1)] in ['A', 'B', 'C', 'D', '#']:stop_left = True
            if self.maze[(x, y_2+1)] in ['A', 'B', 'C', 'D', '#']:stop_right = True

            # Move amphipod to the left
            if not stop_left:y_1 -= 1

            # Move amphipod to the right
            if not stop_right:y_2 += 1

            new_cur_cost += self.cost

            # Check if amphipod is above desitnation
            if y_1 == goal[0][1] or y_2 == goal[0][1]:
                # Check if the destination is valid
                tmp = [self.maze[p[0]][p[1]] if self.maze[p[0]][p[1]] in [self.type, '.'] else None for p in goal]
                if None in tmp: continue

                # x index to the goal
                try:
                    new_x = tmp.index(self.type)+1
                except ValueError:
                    new_x = 5
                # y index to the goal and new cost
                if y_1 == goal[0][1]:
                    new_y = y_1
                else:
                    new_y = y_2
                new_cost = new_cur_cost+(new_x-1)*self.cost
                
                # new maze
                new_maze = copy.copy(self.maze)
                new_maze[new_x][new_y] = self.type
                new_maze[self.x][self.y] = '.'
                
                # Got to correct position, therefore drop the other possible positions.
                children = []

                if self.cor_pos+1 == 16:
                    return [Amphipod(type=self.type, x=new_x, y= new_y, maze=new_maze, cost=self.cost, cur_cost=new_cost, cor_pos=self.cor_pos+1, parent=self)]

                for i, j in positions:
                    val = new_maze[i][j]
                    if val not in ['A', 'B', 'C', 'D']: continue

                    # Check if the destination is valid and the amphipod has to be in the hallway
                    goal_ = goals[val]
                    p1 = new_maze[goal_[0][0]][goal_[0][1]]
                    p2 = new_maze[goal_[1][0]][goal_[1][1]]
                    p3 = new_maze[goal_[2][0]][goal_[2][1]]
                    p4 = new_maze[goal_[3][0]][goal_[3][1]]
                    if (i, j) == goal_[3] or ((i, j) == goal_[2] and  p4 == val) or ((i, j) == goal_[1] and p4==p3==val) or ((i, j) == goal_[0] and p4==p3==p2): continue

                    # Desitnation is valid, can move from hallway
                    n = Counter([p1, p2, p3, p4])
                    if ((n[val]+n['.']) == 4) and i == 1 and not blocking_amphipod(new_maze, j, goal_[0][1]):
                        children.append(Amphipod(type=val, x=i, y=j, maze=new_maze, cost=costs[val], cur_cost=new_cost, cor_pos=self.cor_pos+1, parent=self))

                    # Move alphipod from unvalid slot to the hallway
                    elif i != 1 and new_maze[i-1][j] == '.':
                        children.append(Amphipod(type=val, x=i, y=j, maze=new_maze, cost=costs[val], cur_cost=new_cost, cor_pos=self.cor_pos+1, parent=self))
                break

            for t, y in enumerate([y_1, y_2]):
                if t == 0 and stop_left: continue
                if t == 1 and stop_right: continue
                if self.maze[x+1][y] == "#":
                    # new maze
                    new_maze = copy.copy(self.maze)
                    new_maze[x][y] = self.type
                    new_maze[self.x][self.y] = '.'

                    for i, j in positions: 
                        val = new_maze[i][j]
                        if val not in ['A', 'B', 'C', 'D']: continue

                        # Check if the destination is valid and the amphipod has to be in the hallway
                        goal_ = goals[val]
                        p1 = new_maze[goal_[0][0]][goal_[0][1]]
                        p2 = new_maze[goal_[1][0]][goal_[1][1]]
                        p3 = new_maze[goal_[2][0]][goal_[2][1]]
                        p4 = new_maze[goal_[3][0]][goal_[3][1]]
                        if (i, j) == goal_[3] or ((i, j) == goal_[2] and  p4 == val) or ((i, j) == goal_[1] and p4==p3==val) or ((i, j) == goal_[0] and p4==p3==p2): continue

                        # Destination is valid, can move from hallway
                        n = Counter([p1, p2, p3, p4])
                        if ((n[val]+n['.']) == 4) and i == 1 and not blocking_amphipod(new_maze, j, goal_[0][1]):
                            children.append(Amphipod(type=val, x=i, y=j, maze=new_maze, cost=costs[val], cur_cost=new_cur_cost, cor_pos=self.cor_pos, parent=self))

                        elif i != 1 and new_maze[i-1][j] == '.':
                            children.append(Amphipod(type=val, x=i, y=j, maze=new_maze, cost=costs[val], cur_cost=new_cur_cost, cor_pos=self.cor_pos, parent=self))
        
        return children


def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    return np.asarray([[c for c in line]+['#'for i in range(13-len(line))] for line in open(infile).read().replace(' ', '#').split('\n')])

def blocking_amphipod(maze, y_amp, y_dest):
    if y_amp < y_dest:
        return Counter(maze[1][y_amp+1:y_dest+1])['.'] != (y_dest-y_amp)
    else:
        return Counter(maze[1][y_dest:y_amp])['.'] != (y_amp-y_dest)

def find_init_cor_pos(maze):
    global positions, goals
    count = 0
    for i, j in positions:
        val = maze[i][j]
        if val not in ['A', 'B', 'C', 'D']: continue
        # Check if the destination is valid and the amphipod has to be in the hallway
        goal_ = goals[val]
        p1 = maze[goal_[0][0]][goal_[0][1]]
        p2 = maze[goal_[1][0]][goal_[1][1]]
        p3 = maze[goal_[2][0]][goal_[2][1]]
        p4 = maze[goal_[3][0]][goal_[3][1]]
        if (i, j) == goal_[3] or ((i, j) == goal_[2] and  p4 == val) or ((i, j) == goal_[1] and p4==p3==val) or ((i, j) == goal_[0] and p4==p3==p2): count += 1
    return count

def print_steps(last_amphipod):
    steps = []
    cost = last_amphipod.cur_cost
    cur_amphipod = last_amphipod
    while cur_amphipod:
        steps.append(cur_amphipod.maze)
        cur_amphipod = cur_amphipod.parent
    for maze in steps[::-1]:
        for i in range(7):
            for j in range(13):
                print(maze[i][j], end='')
            print()
        print()
    print("Total cost:", cost)

def change_maze(maze):
    new_maze = list()
    for i, row in enumerate(maze):
        new_maze.append(row)
        if i == 2:
            new_maze += [["#", '#', '#', 'D', '#', 'C', '#', 'B', '#', 'A', '#', '#', '#'],
                        ["#", '#', '#', 'D', '#', 'B', '#', 'A', '#', 'C', '#', '#', '#']]
    return np.asarray(new_maze)

def find_seq(maze):
    global costs, positions
    amphipods = list()
    # Set up the initial state
    maze = change_maze(maze)
    n = find_init_cor_pos(maze)
    for x, y in [(2, 3), (2, 5), (2, 7), (2, 9)]:amphipods.append(Amphipod(type=maze[x][y], x=x, y=y, maze=maze, cost=costs[maze[x][y]], cur_cost=0, cor_pos=n))
    heapq.heapify(amphipods)
    found = False
    visited = {tuple(amphipod.maze[x][y] for x, y in positions) for amphipod in amphipods}
    cur_costs = defaultdict(lambda:99999)
    while not found:
        amphipod = heapq.heappop(amphipods)
        if amphipod.cor_pos == 16:
            found = True
            print_steps(amphipod)
        tmp = tuple(amphipod.maze[x][y] for x, y in positions)
        children = amphipod.calc_moves()
        v = defaultdict(int)
        for child in children:
            tmp = tuple(child.maze[x][y] for x, y in positions)
            if tmp in visited:
                if cur_costs[tmp] <= child.cur_cost: continue
            heapq.heappush(amphipods, child)
            v[tmp]=child.cur_cost
        for key, value in v.items():
            cur_costs[key] = value
            visited.add(key)
            

if __name__ == "__main__":
    maze = parse()
    find_seq(maze)