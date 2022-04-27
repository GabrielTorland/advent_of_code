import sys

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    raw = open(infile).read().replace("\n\n", ',').replace('\n', ' ').split(',')
    player_and_cards_raw = [data.split(' ') for data in raw]
    return {data[0] + ' ' + data[1][:len(data[1])-1] : [int(number) for number in data[2:]][::-1] for data in player_and_cards_raw}

def play_game(players_and_cards):
    if len(players_and_cards["Player 1"]) == 0:
        print("Player 2 won!")
        return players_and_cards
    elif len(players_and_cards["Player 2"]) == 0:
        print("Player 1 won!")
        return players_and_cards
    player_1_card = players_and_cards["Player 1"].pop()
    player_2_card = players_and_cards["Player 2"].pop()
    if player_1_card > player_2_card:
        players_and_cards["Player 1"].insert(0, player_1_card)
        players_and_cards["Player 1"].insert(0, player_2_card)
    else:
        players_and_cards["Player 2"].insert(0, player_2_card)
        players_and_cards["Player 2"].insert(0, player_1_card)
    return play_game(players_and_cards)

def calulate_winner_score(players_and_cards):
    return [sum([(i+1)*card for i, card in enumerate(cards)]) for cards in players_and_cards.values() if len(cards) > 0][0]


player_and_cards = play_game(parse())
print(calulate_winner_score(player_and_cards))