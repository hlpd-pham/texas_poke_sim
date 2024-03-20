import logging

import pytest

from game import Game
from tests.game.parse_utils import parse_cards, parse_players

from .test_cases.full_house_data import full_house_higher_pair
from .test_cases.one_pair_data import one_pair_1, one_pair_2
from .test_cases.straight_data import higher_straight_broadway, higher_straight_normal
from .test_cases.two_pair_data import two_pair_1_winner


class TestGameTieBreak:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup phase
        logging.info("TestGame setup")
        self.game_instance: Game = Game(num_players=0, debug=True)
        self.test_scenarios = [
            full_house_higher_pair,
            one_pair_1,
            one_pair_2,
            higher_straight_broadway,
            higher_straight_normal,
            two_pair_1_winner,
        ]

        # The yield keyword pauses the fixture here, allowing the test to run with the setup completed
        yield

        # Teardown phase - after yield
        logging.info("TestGame teardown")

    def test_tiebreak_scenarios(self):
        for scenario in self.test_scenarios:
            logging.info(
                f"Tiebreak scenario: {scenario['Title']}----------------------"
            )
            players = parse_players(scenario["Players"])
            for idx, player in enumerate(players):
                self.game_instance.players[idx] = player
            self.game_instance.board = parse_cards(scenario["Board"])
            self.game_instance.get_board()
            winners = self.game_instance.find_winners()
            winner_ids = [player.id for player in winners]
            assert winner_ids == scenario["Winners"]
            logging.info(
                f"------------------------------------------------------------"
            )
