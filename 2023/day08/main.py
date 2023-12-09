import re
from functools import reduce
import math

class Node:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

def parse_input(input_path):
    instructions_raw, nodes_raw = open(input_path, 'r').read().split('\n\n')
    instructions = instructions_raw.strip()
    nodes = {}
    for node_raw in nodes_raw.split('\n'):
        node_name, node_left, node_right = re.search(r"(\w+) = \((\w+), (\w+)\)", node_raw).groups()
        node = Node(node_name, node_left, node_right)
        nodes[node_name] = node
    for node in nodes.values():
        node.left = nodes[node.left]
        node.right = nodes[node.right]
    return instructions, nodes

def part_1(instructions, nodes):
    """Computes the number of steps required to go from node AAA to node ZZZ."""
    current_node = nodes['AAA']
    steps = 0
    while current_node.name != 'ZZZ': 
        instruction = instructions[steps % len(instructions)]
        current_node = current_node.left if instruction == 'L' else current_node.right
        steps += 1
    return steps 

def get_target_steps(instructions, node):
    """Computes the number of steps needed for a node to reach the end."""
    current_node = node
    steps = 0
    while current_node.name[-1] != 'Z':
        instruction = instructions[steps % len(instructions)]
        current_node = current_node.left if instruction == 'L' else current_node.right
        steps += 1
    return steps

def part_2(instructions, nodes):
    """Computes the LCM of the steps, which will be the fewest steps needed for all nodes to reach the end simultaneously."""
    starting_nodes = [node for node in nodes.values() if node.name[-1] == 'A']
    steps_mod_org = [get_target_steps(instructions, node) for node in starting_nodes]
    return reduce(lambda x, y: (x * y) // math.gcd(x, y), steps_mod_org)

def main():
    instructions, nodes = parse_input('input.txt')
    print("Part 1: ", part_1(instructions, nodes)) # 11567
    print("Part 2: ", part_2(instructions, nodes)) # 9858474970153

if __name__ == '__main__':
    main()