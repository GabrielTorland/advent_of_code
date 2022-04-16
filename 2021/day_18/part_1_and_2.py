import math
import heapq
import copy


class binary_tree:
    def __init__(self):
        self.left_val = None
        self.right_val = None
        self.left = None
        self.right = None
        self.parent = None
        self.depth = 0

    def insert_left(self):
        self.left = binary_tree()
        self.left.parent = self 

    def insert_right(self):
        self.right = binary_tree()
        self.right.parent = self

    def insert_val_right(self, val):
        self.right_val = val
    
    def insert_val_left(self, val):
        self.left_val = val

    def update_depth(self, parent_depth):
        self.depth = parent_depth + 1
        
lists = list()


# I represent the list structure as a binary tree.
def parse():
    with open("input.txt", "r") as f:
        for line in f.readlines():        
            a_list = binary_tree()
            current = a_list
            li = line.strip()
            insert_left = True
            current_depth = 0
            for c in li[1:(len(li)-1)]:
                if c == '[':
                    if insert_left: 
                        current.insert_left()
                        current_depth += 1
                        current = current.left
                        current.depth = current_depth
                        insert_left = True
                    else:
                        current.insert_right()
                        current_depth += 1
                        current = current.right
                        current.depth = current_depth
                        insert_left = True
                elif c == ']':
                    current = current.parent
                    current_depth -= 1
                elif c == ',':
                    insert_left = False
                else:
                    if insert_left:
                        current.insert_val_left(int(c))
                    else:
                        current.insert_val_right(int(c))
            lists.append(a_list)        

# Add 1 depth to all nodes in tree
def update_depth(node):
    node.depth += 1
    if node.left != None:
        update_depth(node.left)
    if node.right != None:
        update_depth(node.right)


# Snailfish addion
def addion(x, y):
    root = binary_tree()
    root.depth = -1
    x.parent = root    
    root.left = x
    y.parent = root
    root.right = y
    update_depth(root)
    
    return root

# Look for literal value in a right branch.
# If found, the value is added.
def explode_branch_right(node, value):
    state = False
    if node.left == None:
        node.left_val += value
        return True
    state = explode_branch_right(node.left, value)
    if state:
         return True
    if node.right == None:
        node.right_val += value
        return True
    state = explode_branch_right(node.right, value)
    return state

# Look for literal value in a left branch
# If found the value is added
def explode_branch_left(node, value):
    if node.right == None:
        node.right_val += value
        return True
    state = explode_branch_left(node.right, value)
    if state:
         return True
    if node.left == None:
        node.left_val += value
        return True
    state = explode_branch_left(node.left, value)
    return state
        
def explode(node, right_val, left_val, left_found, right_found, prev):
    found_left = left_found
    found_right = right_found
    # Check is the child node to the right is already explodred and not found.
    if (prev is not node.left) and (not left_found):
        # If there are any child nodes, seach them.
        if (node.left != None):
            found_left = explode_branch_left(node.left, left_val)
        else:
            # Found a literal value to the left.
            node.left_val += left_val
            found_left = True
    # Check is the child node to the left is already explodred and not found.
    if (prev is not node.right) and (not right_found):
        if (node.right != None):
            found_right = explode_branch_right(node.right, right_val)
        else:
            # Found a literal value to the right.
            node.right_val += right_val
            found_right = True
    # Reached root node or found left and right literal values, explode finished.
    if node.parent == None or (left_found and right_found):
        return
    # Go up the tree to search for more literal values.
    explode(node.parent, right_val, left_val, found_left, found_right, node)

def detect_explotions(node, child):
    explotions = 0
    if node.depth == 4:
        parent = node.parent
        right_val = node.right_val
        left_val = node.left_val
        if child == "left":
            node.parent.left_val = 0    
            explode(parent, right_val, left_val, False, False, node)    
            node.parent.left = None
        else:
            node.parent.right_val = 0
            explode(parent, right_val, left_val, False, False, node)    
            node.parent.right = None
        explotions += 1
    if node.left != None:
        explotions += detect_explotions(node.left, "left")
    if node.right != None:
        explotions += detect_explotions(node.right, "right")
    return explotions

def split(node):
    count = 0
    if node.left != None:
        count += split(node.left)
        if count == 1:
            return count
    else:
        if node.left_val >= 10:
            node.insert_left()
            node.left.insert_val_left(math.floor(node.left_val/2))
            node.left.insert_val_right(math.ceil(node.left_val/2))
            node.left.update_depth(node.depth)
            node.left_val = None
            count += 1
            return count
    if node.right != None:
        count += split(node.right)
        if count == 1:
            return count
    else:
        if node.right_val >= 10:
            node.insert_right()
            node.right.insert_val_left(math.floor(node.right_val/2))
            node.right.insert_val_right(math.ceil(node.right_val/2))
            node.right.update_depth(node.depth)
            node.right_val = None
            count += 1
            return count
    return count

def magnitude_of_sum(node):
    if node.left_val == None:
        left_val = magnitude_of_sum(node.left)
    else:
        left_val = node.left_val
    if node.right_val == None:
        right_val = magnitude_of_sum(node.right)
    else:
        right_val = node.right_val
    return 3*left_val + 2*right_val

def print_tree(node):
    if node.left != None:
        print_tree(node.left)
    else:
        print(node.left_val, end=", ")
    if node.right != None:
        print_tree(node.right)
    else:
        print(node.right_val, end=", ")

# Take in two list and calculate the 'sum', then reduction.
def addion_and_reduction(x, y): 
    result = addion(x, y)
    explotions = math.inf
    splits = math.inf
    while explotions != 0 or splits != 0:
        while explotions != 0:
            explotions = detect_explotions(result, None)
        splits = split(result)
        explotions = detect_explotions(result, None)
    return result

def part_1():
    x = lists[0]
    for y in lists[1:]:
        x = addion_and_reduction(x, y)

        # Used for testing
        print_tree(x)
        print()
    print(magnitude_of_sum(x))


def part_2():
    results = []
    for i, x in enumerate(lists_copy):
        for j, y in enumerate(lists_copy):
            if i != j:
                result = addion_and_reduction(copy.deepcopy(x), copy.deepcopy(y))
                results.append(magnitude_of_sum(result))
                result = addion_and_reduction(copy.deepcopy(y), copy.deepcopy(x))
                results.append(magnitude_of_sum(result))
    print(len(results))
    heapq._heapify_max(results)
    print(heapq._heappop_max(results))


parse()
lists_copy = copy.deepcopy(lists)

part_1()
part_2()

