import sys

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'test.in'
    data = open(infile, 'r').read().split('\n')
    return {"player 1": data[0][-1], "player 2": data[1][-1]}

def player_move(player_position, player_score, dices_trown):
    rng = sum(range(dices_trown+1, dices_trown+4))
    next =  player_position+rng
    player_position = next % 10
    player_score += player_position+1
    return player_position, player_score


def simulate_game(initial_positions, win_score):
    player_1_score = 0
    player_2_score = 0
    player_1_position = int(inital_positions["player 1"])-1
    player_2_position = int(initial_positions["player 2"])-1
    dices_trown = 0
    while True:
        player_1_position, player_1_score= player_move(player_1_position, player_1_score, dices_trown)
        dices_trown += 3
        if player_1_score >= win_score:
            return player_2_score*dices_trown
        player_2_position, player_2_score = player_move(player_2_position, player_2_score, dices_trown)
        dices_trown += 3
        if player_2_score >= win_score:
            return player_1_score*dices_trown

            


if __name__ == '__main__':
    inital_positions = parse()
    print(simulate_game(inital_positions, 1000))
