import sys

def win(o):
    """_summary_
        Returns the score for winning against o
    Args:
        o (string) : opponent's move

    Returns:
        int : score 
    """    
    match o:
        case "A":
            return 8
        case "B":
            return 9
        case "C":
            return 7 
def lose(o):
    """_summary_
        Returns the score for losing to o
    Args:
        o (string): opponent's move

    Returns:
        int: score 
    """    
    match o:
        case "A":
            return 3
        case "B":
            return 1 
        case "C":
            return 2 


def score(i , o):
    """_summary_
        Calculates the score for a given instruction 
    Args:
        i (string):  outcome
        o (string): opponent's move 

    Returns:
        int : score 
    """    
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