import logging

from card import CardDealAmount
from game import Game
from utils.strings import to_string

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",
    )
    num_players = 1
    players_and_dealer = num_players + 1
    print(f"start game-----------------------------------")
    game = Game(num_players=players_and_dealer, debug=True)
    dealer_id = list(game.players.keys())[-1]

    player_ids = set([p_id for p_id in game.players.keys()]).remove(dealer_id)
    print("player cards")
    for p in game.players.values():
        print(to_string(p.cards))

    print("dealer cards:", to_string(game.players[dealer_id].cards))

    decision = input("Player make decision: ([P]lay, [F]old) > ")

    game.dealing_to_board(CardDealAmount.FLOP)
    print("board")
    print(to_string(game.get_board()))

    decision = input("Player make decision: ([P]lay, [F]old) > ")

    game.dealing_to_board(CardDealAmount.TURN)
    game.dealing_to_board(CardDealAmount.RIVER)
    print("board")
    print(to_string(game.get_board()))

    print("hand results")
    game._evaluating_player_hands()
    for player in game.players.values():
        print(f"id:{player.id}, {to_string(player.cards)}, {player.hand_result}")

    print("winners")
    winners = game.find_winners()
    for w in winners:
        print(f"id:{w.id}, {to_string(w.cards)}, {w.hand_result}")

    if dealer_id in [w.id for w in winners]:
        print("dealer wins")
    else:
        print("players win")
    print(f"end game-----------------------------------")
