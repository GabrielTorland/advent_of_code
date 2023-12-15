from collections import defaultdict

def parse_input(input_path):
    return open(input_path, 'r').read().replace('\n', '').split(',')

def hash_algorithm(step):
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256 
    return current_value

def part_1(steps):
    total_hash_value = 0
    for step in steps:
        total_hash_value += hash_algorithm(step)
    return total_hash_value

def part_2(steps):
    """
    Calculate the focusing power based on the given steps.
    """
    boxes = defaultdict(list)
    for step in steps:
        if '=' in step:
            label, focal_length = step.split('=')
            focal_length = int(focal_length)
            box_id = hash_algorithm(label)
            for i, lens in enumerate(boxes[box_id]):
                if lens[0] == label:
                    boxes[box_id][i] = (label, focal_length)
                    break
            else:
                boxes[box_id].append((label, focal_length))
        else:
            label = step[:-1]
            box_id = hash_algorithm(label)
            boxes[box_id] = [(l, f) for l, f in boxes[box_id] if l != label]
    focusing_power = 0
    for box_id, lenses in boxes.items():
        focusing_power += sum([(box_id+1)*lens[1]*(i+1) for i, lens in enumerate(lenses)])
    return focusing_power


def main():
    input_path = 'input.txt'
    steps = parse_input(input_path)
    print("Part 1: ", part_1(steps)) # 514025
    print("Part 2: ", part_2(steps)) # 244461


if __name__ == '__main__':
    main()


