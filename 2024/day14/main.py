import re

class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def __eq__(self, other):
        if isinstance(other, Robot):
            return self.x == other.x and self.y == other.y
        else:
            return self.x ==other[0] and self.y == other[1]

def parse(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    position_pattern = re.compile(r"p=(\d+),(\d+)")
    velocity_pattern = re.compile(r"v=(-?\d+),(-?\d+)")

    robots = []
    for line in lines:
        position = position_pattern.search(line)
        velocity = velocity_pattern.search(line)
        x, y = map(int, position.groups())
        vx, vy = map(int, velocity.groups())
        robot = Robot(x, y, vx, vy)
        robots.append(robot)

    return robots

def simulate(time, robots, grid_size_x, grid_size_y):
    for robot in robots:
        robot.x = (robot.x + robot.vx*time) % grid_size_x
        robot.y = (robot.y + robot.vy*time) % grid_size_y
    return robots

def calculate_safety_factor(robots, grid_size_x, grid_size_y):
    safety_factor = 0
    counts = {"quad1": 0, "quad2": 0, "quad3": 0, "quad4": 0}
    mid_x = (grid_size_x - 1) // 2
    mid_y = (grid_size_y - 1) // 2
    for robot in robots:
        match robot.x, robot.y:
            case x, y if x < mid_x and y < mid_y:
                counts["quad1"] += 1
            case x, y if x > mid_x and y < mid_y:
                counts["quad2"] += 1
            case x, y if x < mid_x and y > mid_y:
                counts["quad3"] += 1
            case x, y if x > mid_x and y > mid_y:
                counts["quad4"] += 1

    safety_factor = counts["quad1"] * counts["quad2"] * counts["quad3"] * counts["quad4"]
    return safety_factor

def plot_grid(robots, grid_size_x, grid_size_y, output_file="grid_plot.txt"):
    with open(output_file, 'w') as f:
        for i in range(grid_size_y):
            line = []
            for j in range(grid_size_x):
                count = robots.count((j, i))
                line.append("#" if count else ".")
            f.write("".join(line) + "\n")

def find_christmas_tree(height, robots, grid_size_x, grid_size_y):
    for robot in robots:
        if (robot.x + height) >= grid_size_x or (robot.x-height) <= 0 \
             or (robot.y + height) >= grid_size_y:
            continue
        points =[(x, y) for y in range(robot.y+1, robot.y+height) for x in range(robot.x-1*(y-robot.y), robot.x+(y-robot.y)+1)]
        if all(point in robots for point in points):
            return robot.x, robot.y

if __name__ == "__main__":
    input_file = "input.txt"
    robots = parse(input_file)
    if input_file == "test.txt":
        grid_size_x = 11
        grid_size_y = 7
    else:
        grid_size_x = 101
        grid_size_y = 103

    robots = simulate(100, robots, grid_size_x, grid_size_y)
    #plot_grid(robots, grid_size_x, grid_size_y)
    safety_factor = calculate_safety_factor(robots, grid_size_x, grid_size_y)
    print("Part 1:", safety_factor)

    for i in range(100000):
        robots = simulate(1, robots, grid_size_x, grid_size_y)
        if find_christmas_tree(5, robots, grid_size_x, grid_size_y):
            print("Part 2:", 100+i+1)
            break