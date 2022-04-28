import sys

def simulate(seq, rounds, current_round):
    if current_round == rounds+1:
        return seq
    current_val = seq[0]
    pick_up = seq[1:4]
    destination = current_val-1
    while destination != 0:
        if destination not in pick_up:
            break
        else:
            destination = destination-1
    if destination == 0:
        destination = max(seq[4:])
    new_seq = seq[4:seq.index(destination)+1] + pick_up + seq[seq.index(destination)+1:] + [current_val]
    return simulate(new_seq, rounds, current_round+1)
    
def calculate_order(seq):
    return ''.join(map(str, seq[seq.index(1)+1:] + seq[:seq.index(1)]))

seq = sys.argv[1] if len(sys.argv) > 1 else "463528179"
seq = [int(c) for c in seq]
seq = simulate(seq, 100, 1)
print(calculate_order(seq))