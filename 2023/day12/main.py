

def parse_input(input_path):
    with open(input_path) as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        record, cont_broken = line.split()
        cont_broken = [int(x) for x in cont_broken.split(',')]
        yield record, cont_broken

def get_number_of_record_combinations(record, cont_broken, cont_broken_idx, record_idx, memo): 
    """Compute all possible record combinations given a record and a list of continuous broken springs."""
    total_combinations = 0
    for i in range(record_idx, len(record)):
        if i + cont_broken[cont_broken_idx] > len(record): break
        # Not possible to skip broken records
        if any(record[j] == '#' for j in range(record_idx, i)): break 
        # Continues broken springs can't contain working spring 
        if any(record[j] == '.' for j in range(i, i + cont_broken[cont_broken_idx])): 
            continue 
        # Skip if next spring is broken
        if i + cont_broken[cont_broken_idx] < len(record) and record[i + cont_broken[cont_broken_idx]] == '#': 
            continue
        new_record = record[:i] + '#'*cont_broken[cont_broken_idx] + record[i + cont_broken[cont_broken_idx]:] 
        if cont_broken_idx == len(cont_broken) - 1: 
            if any(new_record[j] == '#' for j in range(i + cont_broken[cont_broken_idx], len(new_record))): continue
            total_combinations += 1
        else:
            if (i + cont_broken[cont_broken_idx] + 1) >= len(record): continue 
            if (cont_broken_idx+1, i+cont_broken[cont_broken_idx]+1) in memo:
                sub_comb = memo[(cont_broken_idx+1, i+cont_broken[cont_broken_idx]+1)]
            else:
                sub_comb = get_number_of_record_combinations(new_record, cont_broken, cont_broken_idx + 1, i + cont_broken[cont_broken_idx] + 1, memo) 
            memo[(cont_broken_idx+1, i+cont_broken[cont_broken_idx]+1)] = sub_comb
            total_combinations += sub_comb
    return total_combinations 

def part_1(input_path):
    total_combinations = 0
    for record, cont_broken in parse_input(input_path):
        total_combinations += get_number_of_record_combinations(record, cont_broken, 0, 0, {})
    return total_combinations

def part_2(input_path):
    total_combinations = 0
    for record, cont_broken in parse_input(input_path):
        record = "?".join(record for _ in range(5)) 
        cont_broken = [cont_broken[i%len(cont_broken)] for i in range(5*len(cont_broken))] 
        total_combinations += get_number_of_record_combinations(record, cont_broken, 0, 0, {})
    return total_combinations

def main():
    input_path = "input.txt"
    print("Part 1: ", part_1(input_path)) # 7350
    print("Part 2: ", part_2(input_path)) # 200097286528151



if __name__ == '__main__':
    main() 