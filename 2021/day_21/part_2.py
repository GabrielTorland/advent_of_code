import sys
from functools import lru_cache


def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    data = open(infile, 'r').read().split('\n')
    return {"player 1": data[0][-1], "player 2": data[1][-1]}


@lru_cache(maxsize=None)
def simulate_games_(*args):
    if args[3] >= 21: return (0, 1)

    p1_wins, p2_wins = 0, 0
    
    # r is the sum of the three dieces ad f is the repetition factor.
    # I found these permutations by hand :D
    for r, f in [(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]:
        next_pos = (args[0]+r)%10
        w_2, w_1 = simulate_games_(args[2], args[3], next_pos, args[1]+next_pos+1)
        p1_wins += w_1*f
        p2_wins += w_2*f
    
    return p1_wins, p2_wins
 
        

if __name__ == '__main__':
    initial_positions = parse()
    p1_wins, p2_wins = simulate_games_(int(initial_positions["player 1"])-1, 0, int(initial_positions["player 2"])-1, 0)
    print("Part 2:", max(p1_wins, p2_wins))

