import numpy as np

def parse_input(input_path='input.txt'):
    raw_notes = open(input_path, 'r').read().split('\n\n')
    for raw_note in raw_notes:
        note = np.array([np.array([val for val in row.strip()]) for row in raw_note.split('\n')])
        yield note

def get_horizontal_symmetry_line(note):
    symmetry_lines = []
    for i in range(len(note)-1):
        if not np.array_equal(note[i], note[i+1]): continue
        for j in range(min(len(note)-i-2, i)):
            if not np.array_equal(note[i-j-1], note[i+j+2]): break 
        else:
            symmetry_lines.append(i) 
    return symmetry_lines

def get_vertical_symmetry_line(note):
    symmetry_lines = []
    for i in range(len(note[0])-1):
        if not np.array_equal(note[:,i], note[:,i+1]): continue
        for j in range(min(len(note[0])-i-2, i)):
            if not np.array_equal(note[:,i-j-1], note[:,i+j+2]):break 
        else:
            symmetry_lines.append(i)
    return symmetry_lines

def get_nudge_horizontal_symmetry_line(note):
    for i in range(len(note)-1):
        count = 0
        for j in range(min(len(note)-i-1, i+1)):
            for val_1, val_2 in zip(note[i-j], note[i+j+1]):
                count += 1 if val_1 != val_2 else 0
                if count > 1:
                    break
            if count > 1: 
                break
        else:
            if count == 1:
                return i
    return

def get_nudge_vertical_symmetry_line(note):
    for i in range(len(note[0])-1):
        count = 0
        for j in range(min(len(note[0])-i-1, i+1)):
            for val_1, val_2 in zip(note[:,i-j], note[:,i+j+1]):
                count += 1 if val_1 != val_2 else 0
                if count > 1: break
            if count > 1: break
        else:
            if count == 1:
                return i
    return

def summarize_correct_symmetry_line(note, horizontal_symmetry_lines, vertical_symmetry_line):
    areas = []
    summary_numbers = []
    for i in horizontal_symmetry_lines:
        areas.append(min(i+1, len(note)-i-1)*note.shape[1])
        summary_numbers.append((i+1)*100)
    for i in vertical_symmetry_line:
        areas.append(min(i+1, len(note[0])-i-1)*note.shape[0])
        summary_numbers.append(i+1)
    return summary_numbers[areas.index(max(areas))]

def part_1(notes):
    total = 0 
    for note in notes:
        horizontal_symmetry_lines = get_horizontal_symmetry_line(note)
        vertical_symmetry_line = get_vertical_symmetry_line(note)
        total += summarize_correct_symmetry_line(note, horizontal_symmetry_lines, vertical_symmetry_line)
    return total

def part_2(notes):
    total = 0
    for note in notes:
        horizontal_symmetry_line = get_nudge_horizontal_symmetry_line(note)
        if horizontal_symmetry_line is not None:
            total += (horizontal_symmetry_line+1)*100
        vertical_symmetry_line = get_nudge_vertical_symmetry_line(note)
        if vertical_symmetry_line is not None:
            total += (vertical_symmetry_line+1)
        if vertical_symmetry_line and horizontal_symmetry_line:
            np.savetxt('output.txt', note, fmt='%s')
            print()
    return total


def main():
    notes = parse_input()
    print("Part 1: ", part_1(notes)) # 31739
    notes = parse_input()
    print("Part 2: ", part_2(notes)) # 31539


if __name__ == '__main__':
    main()

