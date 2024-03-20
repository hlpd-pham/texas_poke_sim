import logging

from card import CardDealAmount
from game import Game
from utils.strings import to_string

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",
)


def run():
    num_players = 5
    print(f"start game for {num_players} players")
    game = Game(num_players=num_players, debug=True)

    for deal_type in [CardDealAmount.FLOP, CardDealAmount.TURN, CardDealAmount.RIVER]:
        game.dealing_to_board(deal_type)

    print("board")
    print(to_string(game.get_board()))
    print()

    print("hand results")
    game._evaluating_player_hands()
    for player in game.players.values():
        print(f"id:{player.id}, {to_string(player.cards)}, {player.hand_result}")

    print("winners")
    for w in game.find_winners():
        print(f"id:{w.id}, {to_string(w.cards)}, {w.hand_result}")


run()
