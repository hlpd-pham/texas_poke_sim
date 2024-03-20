import logging
from unittest.mock import patch

import pytest

from card import CardDealAmount
from game import Game
from game_evaluator import HandResult

from ..fixtures.game_mock_data import mock_card_options


class TestGame:

    def make_mock_cards(self, num_players=1):
        def mock_cards(*args, **kwargs):
            ret = []
            cards_for_players = 2 * num_players
            match self.call_count:
                case 0:
                    ret = mock_card_options[:cards_for_players]  # deal to player
                case 1:
                    ret = mock_card_options[
                        cards_for_players : cards_for_players + 1
                    ]  # burn for flop
                case 2:
                    ret = mock_card_options[
                        cards_for_players + 1 : cards_for_players + 4
                    ]  # flop
                case 3:
                    ret = mock_card_options[
                        cards_for_players + 4 : cards_for_players + 5
                    ]  # burn for turn
                case 4:
                    ret = mock_card_options[
                        cards_for_players + 5 : cards_for_players + 6
                    ]  # turn
                case 5:
                    ret = mock_card_options[
                        cards_for_players + 6 : cards_for_players + 7
                    ]  # burn for river
                case 6:
                    ret = mock_card_options[
                        cards_for_players + 7 : cards_for_players + 8
                    ]  # river
                case _:
                    ret = []
            self.call_count += 1
            return ret

        return mock_cards

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup phase
        logging.info("TestGame setup")
        self.call_count = 0
        with patch("random.sample", side_effect=self.make_mock_cards()):
            self.game_instance: Game = Game(num_players=1, debug=True)

        # The yield keyword pauses the fixture here, allowing the test to run with the setup completed
        yield

        # Teardown phase - after yield
        logging.info("TestGame teardown")

    def test_game_init(self):
        """expect initialization states with 1 player"""
        assert len(self.game_instance.players) == 1
        assert len(self.game_instance.deck) == 50
        assert len(self.game_instance.get_board()) == 0
        assert self.game_instance._debug

    def test_game_init_bad_input(self):
        with pytest.raises(ValueError, match="Invalid number of players: "):
            self.game_instance: Game = Game(num_players=-1)

    def test_game_deal_card_not_in_deck(self):
        with pytest.raises(ValueError, match="card is not in deck"):
            self.game_instance = Game()
            first_player_id = next(iter(self.game_instance.players))
            dealt_cards = self.game_instance.players[first_player_id].cards
            with patch("random.sample") as mock:
                mock.return_value = dealt_cards
                self.game_instance._deal_card("deal to players", CardDealAmount.PLAYER)

    def test_dealing_to_board_flop(self):
        with patch("random.sample", side_effect=self.make_mock_cards()):
            """expects 3 cards on board after flop"""
            self.game_instance.dealing_to_board(CardDealAmount.FLOP)
            assert (
                len(self.game_instance.get_board()) == 3
            )  # Expect 3 cards on the board after flop
            assert self.game_instance.get_board() == mock_card_options[3:6]

    def test_dealing_to_board_turn(self):
        with patch("random.sample", side_effect=self.make_mock_cards()):
            """expects 4 cards on board after turn"""
            self.game_instance.dealing_to_board(CardDealAmount.FLOP)
            self.game_instance.dealing_to_board(CardDealAmount.TURN)
            assert (
                len(self.game_instance.get_board()) == 4
            )  # Expect 4 cards on the board after turn
            assert (
                self.game_instance.get_board()
                == mock_card_options[3:6] + mock_card_options[7:8]
            )

    def test_dealing_to_board_river(self):
        with patch("random.sample", side_effect=self.make_mock_cards()):
            """expects 5 cards on board after river"""
            self.game_instance.dealing_to_board(CardDealAmount.FLOP)
            self.game_instance.dealing_to_board(CardDealAmount.TURN)
            self.game_instance.dealing_to_board(CardDealAmount.RIVER)
            assert (
                len(self.game_instance.get_board()) == 5
            )  # Expect 5 cards on the board after river
            assert (
                self.game_instance.get_board()
                == mock_card_options[3:6]
                + mock_card_options[7:8]
                + mock_card_options[9:10]
            )

    def test_find_winners_only_1_player(self):
        with patch("random.sample", side_effect=self.make_mock_cards()):
            """expects 5 cards on board after river"""
            for deal_type in [
                CardDealAmount.FLOP,
                CardDealAmount.TURN,
                CardDealAmount.RIVER,
            ]:
                self.game_instance.dealing_to_board(deal_type)
            winners = self.game_instance.find_winners()
            winner = winners[0]
            assert len(winners) == 1
            assert isinstance(winner.hand_result, HandResult)
