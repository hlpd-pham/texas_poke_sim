from card import CardDealAmount
from game import Game


def test_game_run_2_players_should_not_raise():
    game_instance = Game(num_players=2, debug=True)
    game_instance.dealing_to_board(CardDealAmount.FLOP)
    game_instance.dealing_to_board(CardDealAmount.TURN)
    game_instance.dealing_to_board(CardDealAmount.RIVER)
    game_instance.get_board()
