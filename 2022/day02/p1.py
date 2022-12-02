import sys

t = {"X": "A", "Y": "B", "Z": "C"}

def score(m, o):
    global t
    s = 0
    match m:
        case "X":
            s += 1 
        case "Y":
            s += 2
        case "Z":
            s += 3 
    if t[m] == o:
        s += 3
    elif (m == "X" and o == "C") or (m == "Y" and o == "A") or (m == "Z" and o == "B"):
        s += 6
    return s


if __name__ == "__main__":
    moves = open("input.in" if len(sys.argv) == 1 else sys.argv[1], 'r').read().split("\n")
    print(sum([score(move[2], move[0]) for move in moves])) # 11386