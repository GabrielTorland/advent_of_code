
def parse(input_file):
    with open(input_file, 'r') as f:
        raw_data = f.read().split("\n\n")
    warehouse = [[entry for entry in line] for line in raw_data[0].split('\n')]
    instructions = raw_data[1].strip()
    return warehouse, instructions

def get_robot_position(warehouse):
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "@":
                return i, j

def update_warehouse(warehouse, i, j, boxes, di, dj, direction):
    """Updates the warehouse maze. Returns True if any changes were made, False otherwise."""
    if warehouse[i+di][j+dj] == '.':
        warehouse[i][j] = '.'
        warehouse[i+di][j+dj] = '@'
        return True
    elif warehouse[i+di][j+dj] == 'O':
        boxes.append((i+di, j+dj))
        while warehouse[boxes[-1][0]+di][boxes[-1][1]+dj] == 'O':
            boxes.append((boxes[-1][0]+di, boxes[-1][1]+dj))
        if warehouse[boxes[-1][0]+di][boxes[-1][1]+dj] == '.':
            warehouse[i][j] = '.'
            warehouse[i+di][j+dj] = '@'
            for k, l in boxes:
                warehouse[k+di][l+dj] = 'O'
            return True
        else:
            return False
    else:
        return False

def move(pos, boxes, warehouse, direction):
    i, j = pos
    match direction:
        case '>':
            if update_warehouse(warehouse, i, j, boxes, 0, 1, '>'):
                return i, j+1
        case '<':
            if update_warehouse(warehouse, i, j, boxes, 0, -1, '<'):
                return i, j-1
        case '^':
            if update_warehouse(warehouse, i, j, boxes, -1, 0, '^'):
                return i-1, j
        case 'v':
            if update_warehouse(warehouse, i, j, boxes, 1, 0, 'v'):
                return i+1, j
    return i, j

def simulate_warehouse(robot_pos, warehouse, instructions):
    i, j = robot_pos
    for direction in instructions:
        i, j = move((i, j), [], warehouse, direction)

def plot_warehouse(warehouse):
    for line in warehouse:
        print("".join(line))

def calculate_sum_of_gps_coordinates(warehouse):
    rows = len(warehouse)
    cols = len(warehouse[0])
    gps_coordinate_sum = 0
    for i in range(rows):
        for j in range(cols):
            if warehouse[i][j] == 'O':
                gps_coordinate_sum += (i)*100+(j)
    return gps_coordinate_sum

def create_new_warehouse(warehouse):
    new_warehouse = []
    for i in range(0, len(warehouse)):
        new_warehouse.append([])
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == '#':
                new_warehouse[i].append("#")
                new_warehouse[i].append("#")
            elif warehouse[i][j] == 'O':
                new_warehouse[i].append("[")
                new_warehouse[i].append("]")
            elif warehouse[i][j] == '@':
                new_warehouse[i].append("@")
                new_warehouse[i].append(".")
            else:
                new_warehouse[i].append(".")
                new_warehouse[i].append(".")

    return new_warehouse

class Box:
    def __init__(self, left_part, right_part):
        self.left_part = left_part
        self.right_part = right_part

    def __iter__(self):
        return iter([self.left_part, self.right_part])

    def __eq__(self, other):
        return self.left_part == other.left_part and self.right_part == other.right_part

class WarehouseV2:
    def __init__(self, warehouse_map):
        self.warehouse_map = warehouse_map
        self.robot_pos = get_robot_position(warehouse_map)

    def __find_entire_box(self, i, j):
        if self.warehouse_map[i][j] == '[':
            return Box((i, j), (i, j+1))
        else:
            return Box((i, j-1), (i, j))

    def __update_warehouse(self, i, j, di, dj):
        next_object = self.warehouse_map[i+di][j+dj]
        if next_object == '.':
            self.warehouse_map[i][j] = '.'
            self.warehouse_map[i+di][j+dj] = '@'
            return True
        elif next_object in ['[', ']']:
            boxes = [[self.__find_entire_box(i+di, j+dj)]]
            new_boxes_added = True
            if i == 3:
                print()
            while new_boxes_added:
                if len(boxes) > 20:
                    print()
                boxes.append([])
                new_boxes_added = False
                for left_part, right_part in boxes[-2]:
                    if self.warehouse_map[left_part[0]+di][left_part[1]+dj] in ['[', ']']:
                        new_box = [self.__find_entire_box(left_part[0]+di, left_part[1]+dj)]
                        if new_box[0] not in boxes[-2]:
                            boxes[-1] += new_box
                            new_boxes_added = True
                    if self.warehouse_map[right_part[0]+di][right_part[1]+dj] in ['[', ']']:
                        new_box = [self.__find_entire_box(right_part[0]+di, right_part[1]+dj)]
                        if not new_box[0] in boxes[-2]:
                            boxes[-1] += new_box
                            new_boxes_added = True
            boxes.pop()
            for box_line in boxes:
                for box in box_line:
                    if self.warehouse_map[box.left_part[0]+di][box.left_part[1]+dj] == '#'\
                        or self.warehouse_map[box.right_part[0]+di][box.right_part[1]+dj] == '#':
                        return False
            for boxes_layer in boxes[::-1]:
                for box in boxes_layer:
                    self.warehouse_map[box.left_part[0]][box.left_part[1]] = '.'
                    self.warehouse_map[box.right_part[0]][box.right_part[1]] = '.'
                    self.warehouse_map[box.left_part[0]+di][box.left_part[1]+dj] = '['
                    self.warehouse_map[box.right_part[0]+di][box.right_part[1]+dj] = ']'
            self.warehouse_map[i][j] = '.'
            self.warehouse_map[i+di][j+dj] = '@'
            return True
        else:
            return False


    def move(self, direction):
        i, j = self.robot_pos
        match direction:
            case '>':
                if self.__update_warehouse(i, j, 0, 1):
                    self.robot_pos = i, j+1
            case '<':
                if self.__update_warehouse(i, j, 0, -1):
                    self.robot_pos = i, j-1
            case '^':
                if self.__update_warehouse(i, j, -1, 0):
                    self.robot_pos = i-1, j
            case 'v':
                if self.__update_warehouse(i, j, 1, 0):
                    self.robot_pos = i+1, j
    def calculate_sum_of_gps_coordinates(self):
        rows = len(self.warehouse_map)
        cols = len(self.warehouse_map[0])
        gps_coordinate_sum = 0
        for i in range(rows):
            for j in range(cols):
                if self.warehouse_map[i][j] == '[':
                    gps_coordinate_sum += (i)*100+(j)
        return gps_coordinate_sum


def count_walls(warehouse):
    return sum(1 for line in warehouse for entry in line if entry == '#')

def p1(warehouse, instructions):
    simulate_warehouse(get_robot_position(warehouse), warehouse, instructions)
    return calculate_sum_of_gps_coordinates(warehouse)

def p2(warehouse, instructions):
    warehouse = create_new_warehouse(warehouse)
    warehouse = WarehouseV2(warehouse)
    for direction in instructions:
        warehouse.move(direction)
    plot_warehouse(warehouse.warehouse_map)
    return warehouse.calculate_sum_of_gps_coordinates()

if __name__ == "__main__":
    warehouse, instructions = parse("input.txt")
    print("Part 1:", p1(warehouse, instructions))
    warehouse, instructions = parse("input.txt")
    print("Part 2:", p2(warehouse, instructions))