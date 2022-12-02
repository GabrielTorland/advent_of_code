import sys

def win(o):
    match o:
        case "A":
            return 8
        case "B":
            return 9
        case "C":
            return 7 
def lose(o):
    match o:
        case "A":
            return 3
        case "B":
            return 1 
        case "C":
            return 2 


def score(i , o):
    t = {"A": 1, "B": 2, "C": 3}
    s = 0
    if i ==  "X":
       s += lose(o) 
    elif i == "Y":
        s += t[o] + 3
    else:
        s += win(o)
    return s

if __name__ == "__main__":
    moves = open("input.in" if len(sys.argv) == 1 else sys.argv[1], 'r').read().split("\n")
    print(sum([score(move[2], move[0]) for move in moves])) # 13600