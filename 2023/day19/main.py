from dataclasses import dataclass 
import re
import math

@dataclass
class Condition:
    attribute: str
    operator: str
    value: int 
    next_workflow_id: str 

    def check_condition(self, part):
        """Checks if the part satisfies the condition."""
        if self.attribute is None:
            return True
        part_value = getattr(part, self.attribute)
        match self.operator:
            case '>':
                return part_value > self.value
            case '<':
                return part_value < self.value 
            case _:
                raise ValueError("Invalid operator")

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def get_total_rating(self):
        return self.x + self.m + self.a + self.s
    
class Workflow:
    def __init__(self, conditions):
        self.conditions = conditions

    def process_part(self, part):
        """Apply the workflow conditions to the part and returns the next workflow id."""
        for condition in self.conditions:
            if condition.check_condition(part):
                return condition.next_workflow_id 
        return  condition.next_workflow_id 
    
    def get_new_ranges(self, current_part_ranges):
        """Calculates the next possible parts ranges after applying the workflow conditions to the current part ranges."""

        # List with the next possible parts ranges
        new_parts_ranges_workflow = [current_part_ranges.copy()]  
        # Iterate over conditions and create new parts ranges
        for i, condition in enumerate(self.conditions[:-1]):
            rating_type = condition.attribute 
            # Current part range for the rating type
            current_rating_range = new_parts_ranges_workflow[i][rating_type]
            if condition.operator == '<':
                if (condition.value-1) >= current_rating_range[0]: 
                    new_parts_ranges_workflow[i][rating_type] = (current_rating_range[0], min(condition.value-1, current_rating_range[1]))
                    new_parts_ranges_workflow[i] = (new_parts_ranges_workflow[i], condition.next_workflow_id)
                if (condition.value-1) >= current_rating_range[1]: 
                    break 
                next_new_part_ranges = current_part_ranges.copy() if i == 0 else new_parts_ranges_workflow[i][0].copy()
                next_new_part_ranges[rating_type] = (max(condition.value, current_rating_range[0]), current_rating_range[1])
                new_parts_ranges_workflow.append(next_new_part_ranges)
            elif condition.operator == '>':
                if (condition.value+1) <= current_rating_range[1]: 
                    new_parts_ranges_workflow[i][rating_type] = (max(condition.value+1, current_rating_range[0]), current_rating_range[1])
                    new_parts_ranges_workflow[i] = (new_parts_ranges_workflow[i], condition.next_workflow_id)
                if (condition.value+1) <= current_rating_range[0]: 
                    break 
                next_new_part_ranges = current_part_ranges.copy() if i == 0 else new_parts_ranges_workflow[i][0].copy()
                next_new_part_ranges[rating_type] = (current_rating_range[0], min(condition.value, current_rating_range[1]))
                new_parts_ranges_workflow.append(next_new_part_ranges)
            else:
                raise ValueError("Invalid operator")
        else:
            new_parts_ranges_workflow[-1] = (new_parts_ranges_workflow[-1], self.conditions[-1].next_workflow_id)

        return new_parts_ranges_workflow

def parse_input(input_path):
    raw_workflows, raw_parts = open(input_path).read().split('\n\n') 

    workflows = {} 
    for raw_workflow in raw_workflows.split('\n'):
        workflow_id, raw_conditions = re.search(r'(\w+)\{(.+)\}', raw_workflow).groups()
        # Create workflow conditions
        raw_conditions_separated = raw_conditions.split(',')
        conditions = []
        for raw_condition in raw_conditions_separated[:-1]:
            operator = '>' if '>' in raw_condition else '<'
            attribute, rest = raw_condition.split(operator)
            value_raw, next_workflow_id = rest.split(':') 
            conditions.append(Condition(attribute, operator, int(value_raw), next_workflow_id))
        conditions.append(Condition(None, None, None, raw_conditions_separated[-1]))
        # Create workflow
        workflows[workflow_id] = Workflow(conditions)

    parts = []
    for raw_part in raw_parts.split('\n'):
        x, m, a, s = re.search(r'x=(\d+),m=(\d+),a=(\d+),s=(\d+)', raw_part).groups() 
        parts.append(Part(int(x), int(m), int(a), int(s)))
    return workflows, parts

def part_1(workflows, parts):
    """Calculates the sum of the accepted rating numbers."""
    sum_accepted_rating_numbers = 0
    for part in parts:
        workflow_id = 'in'
        while workflow_id not in ['A', 'R']:
            workflow = workflows[workflow_id]
            workflow_id = workflow.process_part(part)
        if workflow_id == 'A':
            sum_accepted_rating_numbers += part.get_total_rating()

    return sum_accepted_rating_numbers

def test_part(possible_parts, part):
    for possible_part in possible_parts:
        if all([start <= value <= end for (start, end), value in zip(possible_part, part)]):
            return True

def part_2(workflows):
    """Calculates the sum of ALL possible accepted rating numbers."""
    sum_total_accepted_rating_numbers = 0
    queue = [({'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}, 'in')]
    possible_parts = []
    while len(queue):
        current_part_ranges, workflow_id = queue.pop(0)
        if workflow_id in ['A', 'R']:
            if workflow_id == 'A':
                sum_total_accepted_rating_numbers += math.prod([(end-start+1) for (start, end) in current_part_ranges.values()])
                possible_parts.append(current_part_ranges.values())
            continue
        workflow = workflows[workflow_id]
        new_parts_ranges_workflow = workflow.get_new_ranges(current_part_ranges)
        queue.extend(new_parts_ranges_workflow)
    return sum_total_accepted_rating_numbers

def main():
    workflows, parts = parse_input('input.txt')
    print("Part 1: ", part_1(workflows, parts)) # 377025
    print("Part 2: ", part_2(workflows)) # 135506683246673

if __name__ == '__main__':
    main()