import logging
import random
from collections import defaultdict
from typing import Dict, List

from card import Card, CardDealAmount
from constants import ALL_CARDS
from game_evaluator import GameEvaluator, HandResult
from player import Player
from utils.strings import to_string


class Game:

    def __init__(self, num_players=1, debug=False):
        if num_players < 0 or num_players > 8:
            raise ValueError(f"Invalid number of players: {num_players}")
        self.game_evaluator = GameEvaluator()
        self._debug: bool = debug
        self.players: Dict[str, Player] = {}
        self.board: List[Card] = []
        self.deck, self.deck_hash = self._get_deck()
        self._poplulate_players(num_players)

    def _get_deck(self):
        deck = ALL_CARDS.copy()
        random.shuffle(deck)
        deck_hash = {card.get_card_value_suite(): card for card in deck}
        return deck, deck_hash

    def _deal_card(
        self, announcement: str, dealing_type: CardDealAmount, is_show=False
    ) -> List[Card]:
        logging.info(announcement)
        cards_dealt: List[Card] = random.sample(self.deck, dealing_type.value)
        if self._debug or is_show:
            logging.info([str(c) for c in cards_dealt])
        for card in cards_dealt:
            if card.get_card_value_suite() not in self.deck_hash:
                raise ValueError(f"card is not in deck: {card} ")
            del self.deck_hash[card.get_card_value_suite()]
        self.deck = list(self.deck_hash.values())
        logging.info(f"cards type {type(self.deck[0])}")
        return cards_dealt

    def _get_kickers_from_hand(
        self, player_cards: List[Card], main_cards: List[Card]
    ) -> List[Card]:
        if len(player_cards) != 7 or len(main_cards) > 5:
            raise ValueError(
                f"player_cards or main_cards not valid: {to_string(player_cards)}, {to_string(main_cards)}"
            )
        # max cards allowed for a hand
        if len(main_cards) == 5:
            return []

        cards_used_for_kickers = 5 - len(main_cards)
        kicker_options = set(player_cards) - set(main_cards)
        sorted_kicker_options = sorted(
            list(kicker_options), key=lambda card: card.get_high_card_value()
        )
        return sorted_kicker_options[-cards_used_for_kickers:]

    def _evaluating_player_hands(self) -> dict[str, Player]:
        logging.info("evaluating player hands")
        logging.info(f"players: {to_string(self.players)}")
        for player_id in self.players.keys():
            player_cards = self.players[player_id].cards + self.board
            hand_result, main_cards = self.game_evaluator.evaluate_hand(player_cards)
            self.players[player_id].hand_result = hand_result
            self.players[player_id].main_cards = sorted(
                main_cards, key=lambda card: card.get_high_card_value()
            )
            self.players[player_id].kickers = self._get_kickers_from_hand(
                player_cards, main_cards
            )
            logging.info(to_string(self.players[player_id]))

        return self.players

    def _poplulate_players(self, num_players) -> None:
        logging.info(f"dealing cards to {num_players} players")
        for idx in range(num_players):
            new_player = Player(id=idx)
            player_cards = self._deal_card(
                f"dealing cards for player {new_player.id}", CardDealAmount.PLAYER
            )
            new_player.cards = player_cards
            self.players[new_player.id] = new_player

    def _find_tie_break_kicker_winners(self, tie_players: List[Player]):
        logging.info(f"tie players need kicker tiebreak {to_string(tie_players)}")
        # no more kicker to tie break
        if not tie_players[0].kickers:
            return tie_players

        highest_kicker_card_value = 0
        kicker_player_map = defaultdict(list)
        for i in range(len(tie_players)):
            player_highest_kicker = tie_players[i].kickers[-1]
            highest_kicker_card_value = max(
                player_highest_kicker.get_high_card_value(), highest_kicker_card_value
            )
            kicker_player_map[player_highest_kicker.get_high_card_value()].append(
                tie_players[i]
            )
            tie_players[i].kickers.pop()

        # still haven't figured out winner
        if len(kicker_player_map[highest_kicker_card_value]) > 1:
            return self._find_tie_break_kicker_winners(tie_players)

        return kicker_player_map[highest_kicker_card_value]

    def _find_tie_break_winners_straight(
        self, tie_players: List[Player]
    ) -> List[Player]:
        broadway_card_values = set([10, 11, 12, 13, 1])
        broadway_players = []
        straight_high_map = defaultdict(list)
        highest_straight_card = 0
        for player in tie_players:
            player_straight_card_values = set(
                [card.value for card in player.main_cards]
            )
            if player_straight_card_values == broadway_card_values:
                broadway_players.append(player)
            else:
                player_highest_straight_card_value = player.main_cards[-1].value
                straight_high_map[player_highest_straight_card_value].append(player)
                highest_straight_card = max(
                    highest_straight_card, player_highest_straight_card_value
                )

        if broadway_players:
            return broadway_players

        return straight_high_map[highest_straight_card]

    def _find_tie_break_winners(self, tie_players: List[Player]) -> List[Player]:
        """
        all tie players should have the same number of main cards for potential
        winning hand
        """
        # need to tie break by kickers
        if not tie_players[0].main_cards:
            return self._find_tie_break_kicker_winners(tie_players)

        if tie_players[0].hand_result == HandResult.STRAIGHT:
            return self._find_tie_break_winners_straight(tie_players)

        highest_main_card_value = 0
        main_card_player_map = defaultdict(list)
        for i in range(len(tie_players)):
            player_highest_main = tie_players[i].main_cards[-1]
            highest_main_card_value = max(
                player_highest_main.get_high_card_value(),
                highest_main_card_value,
            )
            main_card_player_map[player_highest_main.get_high_card_value()].append(
                tie_players[i]
            )
            tie_players[i].main_cards.pop()

        logging.info(
            f"main_card_player_map: {to_string(main_card_player_map)}, highest high card: {highest_main_card_value}"
        )

        # still haven't figured out winner
        if len(main_card_player_map[highest_main_card_value]) > 1:
            return self._find_tie_break_winners(tie_players)

        return main_card_player_map[highest_main_card_value]

    def dealing_to_board(self, dealing_type: CardDealAmount):
        self._deal_card(f"burn 1 for {dealing_type}", CardDealAmount.BURN)
        cards_dealt = self._deal_card(f"{dealing_type}", dealing_type)
        self.board.extend(cards_dealt)

    def get_board(self):
        if self._debug:
            logging.info(f"board cards - {[str(c) for c in self.board]}")
        return self.board

    def find_winners(self) -> List[Player]:
        logging.info("finding hand winner(s)")
        self._evaluating_player_hands()
        score_player_map = defaultdict(list)
        max_score = HandResult.HIGH_CARD.value
        for player in self.players.values():
            player_score = player.hand_result.value
            score_player_map[player_score].append(player)
            max_score = max(max_score, player_score)

        # tie breaking
        if len(score_player_map[max_score]) > 1:
            winners = self._find_tie_break_winners(score_player_map[max_score])
        else:
            winners = score_player_map[max_score]

        logging.info(f"winners: {to_string(winners)}")
        return winners
