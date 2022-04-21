import os
import numpy as np
from collections import defaultdict
import copy

def main():
    rules = dict()
    my_ticket = []
    nearby_tickets = []
    space = 0
    with open(os.path.abspath('input.txt'), 'r') as raw:
        for line in raw:
            if line == '\n':
                space += 1
                continue
            if "ticket" in line:
                continue
            if space == 0:
                temp = line.strip().split(":")
                field = temp[0]
                values = temp[1][1:].split(' ')
                range_1 = values[0].split('-')
                range_1 = [int(val) for val in range_1]
                range_2 = values[2].split('-')
                range_2 = [int(val) for val in range_2] 
                rules[field] = set(range(range_1[0], range_1[1]+1)).union(set(range(range_2[0], range_2[1]+1)))
                
            elif space == 1:
                temp = line.strip().split(",")
                for part in temp:
                    if part.isdigit():
                        my_ticket.append(int(part))
            else:
                temp = line.strip().split(",")
                nearby_ticket = []
                for part in temp:
                    state = False
                    dig = int(part)
                    for rg in rules.values():
                        if dig in rg:
                            state = True
                            break
                    if state:
                        nearby_ticket.append(dig)
                    else:
                        break
                if state:
                    nearby_tickets.append(nearby_ticket)
    return nearby_tickets, rules, my_ticket
    
def create_sets(nearby_tickets, your_ticket):
    fields = [set() for i in range(len(nearby_tickets[0]))]
    iter = nearby_tickets.copy()
    iter.append(your_ticket.copy())
    for ticket in iter:
        for i, number in enumerate(ticket):
            fields[i].add(number)
    return fields

def map_fields(possible_positions, used, i):
    for field in possible_positions[i]:
        if field not in used:
            used.append(field)
            if i == len(possible_positions) - 1:
                return  True, used
            state, temp = map_fields(possible_positions, used, i+1)
            if state:
                return True, temp
            used.pop()
    return False, []

def part_2(neaby_tickets, rules, your_ticket):
    mapping_ticket = dict()
    possible_positions = defaultdict(lambda: set())
    list_of_values = create_sets(neaby_tickets, your_ticket)
    for i, values in enumerate(list_of_values):
        for field in rules.items(): 
            if len(values.difference(field[1])) == 0:
                possible_positions[i].add(field[0])
        if len(possible_positions[i]) == 0:
            return "Impossible"
    state, seq = map_fields(possible_positions, [], 0)
    for i, val in enumerate(your_ticket):
        mapping_ticket[seq[i]] = val
    return mapping_ticket

if __name__ == "__main__":
    nearby_tickets, rules, your_ticket = main()
    mapped_ticket = part_2(nearby_tickets, rules, your_ticket)
    result = 1
    for items in mapped_ticket.items():
        if "departure" in items[0]:
            result *= items[1]
    print(result)