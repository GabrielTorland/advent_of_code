import sys
# If both players have at least as many cards remaining in their deck as the value of the card they just drew, 
# the winner of the round is determined by playing a new game of Recursive Combat.
# Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.


def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    recursion_limit = sys.argv[2] if len(sys.argv) > 2 else "99999999"
    sys.setrecursionlimit(int(recursion_limit))
    raw = open(infile).read().replace("\n\n", ',').replace('\n', ' ').split(',')
    player_and_cards_raw = [data.split(' ') for data in raw]
    return {data[0] + ' ' + data[1][:len(data[1])-1] : [int(number) for number in data[2:]][::-1] for data in player_and_cards_raw}

def play_game(players_and_cards, previous_decks):
    while True:
        if len(players_and_cards["Player 1"]) == 0:
            print("Player 2 won!")
            return players_and_cards, "Player 2"
        elif len(players_and_cards["Player 2"]) == 0:
            print("Player 1 won!")
            return players_and_cards, "Player 1"

        if (tuple(players_and_cards["Player 1"]), tuple(players_and_cards["Player 2"])) in previous_decks:
            print("Player 1 won!")
            return players_and_cards, "Player 1"
        else:
            previous_decks.add((tuple(players_and_cards["Player 1"]), tuple(players_and_cards["Player 2"])))   
        player_1_card = players_and_cards["Player 1"].pop()
        player_2_card = players_and_cards["Player 2"].pop()
        if player_1_card <= len(players_and_cards["Player 1"]) and player_2_card <= len(players_and_cards["Player 2"]):
            new_players_and_cards = players_and_cards.copy()
            for player, cards in new_players_and_cards.items():
                if player == "Player 1":
                    new_players_and_cards[player] = cards[len(players_and_cards["Player 1"]) - player_1_card:]
                else:
                    new_players_and_cards[player] = cards[len(players_and_cards["Player 2"]) - player_2_card:]
            sub_game, winner = play_game(new_players_and_cards, set())
            if winner == "Player 1":
                players_and_cards["Player 1"].insert(0, player_1_card)
                players_and_cards["Player 1"].insert(0, player_2_card)
            else:
                players_and_cards["Player 2"].insert(0, player_2_card)
                players_and_cards["Player 2"].insert(0, player_1_card)
        else:
            if player_1_card > player_2_card:
                players_and_cards["Player 1"].insert(0, player_1_card)
                players_and_cards["Player 1"].insert(0, player_2_card)
            else:
                players_and_cards["Player 2"].insert(0, player_2_card)
                players_and_cards["Player 2"].insert(0, player_1_card)

def calulate_winner_score(players_and_cards, winner):
    return [sum([(i+1)*card for i, card in enumerate(cards)]) for cards in players_and_cards.values() if len(cards) > 0][0]


player_and_cards, winner = play_game(parse(), set())
print(calulate_winner_score(player_and_cards, winner))