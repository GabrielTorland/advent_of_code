import sys

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    data = open(infile, 'r').read().split('\n')
    return {"player 1": data[0][-1], "player 2": data[1][-1]}

def player_move(ply_pos, ply_score, dices_trown):
    rng = (dices_trown+1)*3+3
    next =  ply_pos+rng
    ply_pos = next % 10
    ply_score += ply_pos+1
    return ply_pos, ply_score


def simulate_game(*args):
    dices_trown = 0
    scores = [args[1], args[3]]
    positions = [args[0], args[2]]
    i = 0
    while scores[(i+1)%2] < args[4]:
        positions[i], scores[i] = player_move(positions[i], scores[i], dices_trown)
        dices_trown += 3
        i = (i+1) % 2
    return scores[i]*dices_trown 
            


if __name__ == '__main__':
    inital_positions = parse()
    print(simulate_game(int(inital_positions["player 1"])-1, 0, int(inital_positions['player 2'])-1, 0, 1000))
