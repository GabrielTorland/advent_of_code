import sys
from functools import lru_cache

win_score = 21

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    data = open(infile, 'r').read().split('\n')
    return {"player 1": data[0][-1], "player 2": data[1][-1]}

def player_move(player_position, player_score, dices):
    rng = sum(dices)
    next =  player_position+rng
    player_position = next % 10
    player_score += player_position+1
    return player_position, player_score

@lru_cache(maxsize=None)
def simulate_games(*args):
    """ Game of Dirac dice

    Args:
        state (_tuple_): _game state_

    Returns:
        _list with 2 integers_: _total amount of wins in every dimension_
    """    
    global win_score
    p1_wins = 0
    p2_wins = 0
    for i in range(1, 3+1):
        for j in range(1, 3+1):
            for k in range(1, 3+1):
                player_1_position, player_1_score = player_move(args[0], args[1], [i, j, k])
                if player_1_score >= win_score:
                    p1_wins += 1
                    continue
                for l in range(1, 3+1):
                    for m in range(1, 3+1):
                        for n in range(1, 3+1):
                            player_2_position, player_2_score = player_move(args[2], args[3], [l, m, n])
                            if player_2_score >= win_score:
                                p2_wins += 1
                                continue
                            new_wins = simulate_games(player_1_position, player_1_score, player_2_position, player_2_score)
                            p1_wins += new_wins[0]
                            p2_wins += new_wins[1]
    return p1_wins, p2_wins
  


            


if __name__ == '__main__':
    initial_positions = parse()
    p1_wins, p2_wins = simulate_games(int(initial_positions["player 1"])-1, 0, int(initial_positions["player 2"])-1, 0)
    print(max(p1_wins, p2_wins))

