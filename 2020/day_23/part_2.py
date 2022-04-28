import sys

# Linked list
class Cups:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.lookup = dict()

    # Add several values to the linked list
    def extend(self, seq):
        current = self.end if self.end != None else self.start
        for label in seq:
            current.next = Cup(None, label)
            # Dictionary top look up label of cup
            # Value: Cup object
            self.lookup[label] = current.next
            current = current.next
        self.end = current
# Node in linked list
class Cup:
    def __init__(self, next, label):
        self.next = next
        self.label = label

def simulate(cups):
    """_summary_

    Args:
        cups (_Cups_): _linked list with nodes and lookup dictionary_

    Returns:
        _int_: _Two cups that will end up immediately clockwise of cup 1_
    """    
    for i in range(10*10**6):
        current = cups.start
        pick_up = [cups.start.next, cups.start.next.next.next]
        pick_up_vals = [pick_up[0].label, pick_up[0].next.label, pick_up[1].label]
        destination = current.label-1
        while destination != 0:
            if destination not in pick_up_vals:
                break
            else:
                destination = destination-1
        if destination == 0:
            for i in range(10**6):
                destination = 10**6-i
                if destination not in pick_up_vals and destination != current.label:
                    break

        # Rearranging cups 
        cups.start = pick_up[1].next

        destination_i = cups.lookup[destination]
        temp = destination_i.next
        destination_i.next = pick_up[0]
        pick_up[1].next = temp

        # Special case for 
        if destination == cups.end.label:
            cups.end = pick_up[1]
        cups.end.next = current
        cups.end = current
        cups.end.next = None
    pos_1 = cups.lookup[1]
    return pos_1.next.label*pos_1.next.next.label 


seq = sys.argv[1] if len(sys.argv) > 1 else "463528179"
seq = [int(c) for c in seq]
cup = Cup(None, seq[0])
cups = Cups(cup, None)
cups.lookup[seq[0]] = cup
cups.extend(seq[1:])
cups.extend(range(max(seq)+1, 10**6+1))
print(simulate(cups))
