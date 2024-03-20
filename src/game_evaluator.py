import logging
from collections import defaultdict
from enum import Enum
from typing import List

from card import Card
from utils.strings import to_string


class HandResult(Enum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    PAIR = 2
    HIGH_CARD = 1


class GameEvaluator:
    """This class always assume player cards have 7 cards to make it simple"""

    def _get_pair_cards(self, all_player_cards: List[Card]) -> List[Card]:
        """find the highest pair"""
        value_cards_map = defaultdict(list)
        pair_values = set()
        for c in all_player_cards:
            value_cards_map[c.get_high_card_value()].append(c)
            if len(value_cards_map[c.get_high_card_value()]) >= 2:
                pair_values.add(c.get_high_card_value())

        if not pair_values:
            return []

        pair_values = sorted(list(pair_values))
        highest_pair_value = pair_values[-1]
        return value_cards_map[highest_pair_value]

    def _get_two_pair_cards(self, all_player_cards: List[Card]) -> List[Card]:
        hand_cards = sorted(all_player_cards.copy())
        first_pair_cards = self._get_pair_cards(hand_cards)
        if len(first_pair_cards) == 0:
            return []
        for card in first_pair_cards:
            hand_cards.remove(card)
        second_pair_cards = self._get_pair_cards(hand_cards)
        if len(second_pair_cards) == 0:
            return []
        two_pairs = first_pair_cards + second_pair_cards
        return two_pairs

    def _get_three_of_a_kind_cards(self, all_player_cards: List[Card]) -> List[Card]:
        value_cards_map = defaultdict(list)
        for c in all_player_cards:
            value_cards_map[c.get_high_card_value()].append(c)
            if len(value_cards_map[c.get_high_card_value()]) == 3:
                return value_cards_map[c.get_high_card_value()]
        return []

    def _get_straight_cards(
        self, all_player_cards: List[Card], get_all_cards=False
    ) -> List[Card]:
        """
        only return the highest straight cards if not indicated otherwise
        """
        hand_cards = all_player_cards.copy()
        unique_cards = {}
        for card in hand_cards:
            unique_cards[card.value] = card
        sorted_cards = sorted(unique_cards.values())
        straight_result = []

        if get_all_cards:
            left = 0
            for right in range(1, len(sorted_cards)):
                if not sorted_cards[right - 1].value + 1 == sorted_cards[right].value:
                    left = right

            # check broadway
            if right - left + 1 == 4 and sorted_cards[0].value == 1:
                result = [sorted_cards[0]] + sorted_cards[-4:]
                return result

            # no straight found
            if right - left + 1 < 5:
                return []

            result = sorted_cards[left : right + 1]
            return result

        for straight_end_idx in range(len(sorted_cards) - 1, len(sorted_cards) - 4, -1):
            straight_start_idx = straight_end_idx - 4
            found_straight = True
            for i in range(straight_start_idx, straight_end_idx):
                if not (sorted_cards[i].value + 1 == sorted_cards[i + 1].value):
                    found_straight = False
                    break
            if found_straight:
                straight_result = sorted_cards[
                    straight_start_idx : straight_end_idx + 1
                ]
                break

        # check broadway
        potential_broadway_values = [sorted_cards[0].value] + [
            card.value for card in sorted_cards[-4:]
        ]
        if potential_broadway_values == [1, 10, 11, 12, 13]:
            broadway = [sorted_cards[0]] + sorted_cards[-4:]
            return broadway
        if straight_result:
            return straight_result

        return []

    def _get_flush_cards(
        self, all_player_cards: List[Card], get_all_cards=False
    ) -> List[Card]:
        """
        only return the highest flush cards
        """
        hand_cards = sorted(all_player_cards)
        suite_cards_map = defaultdict(list)
        flush_suite = None
        for card in hand_cards:
            suite_cards_map[card.suit].append(card)
            if len(suite_cards_map[card.suit]) >= 5:
                flush_suite = card.suit

        if flush_suite:
            flush_cards = suite_cards_map[flush_suite]
            result = sorted(flush_cards, key=lambda card: card.get_high_card_value())
            if get_all_cards:
                return result
            result = result[-5:]
            return result

        return []

    def _get_full_house_cards(self, all_player_cards: List[Card]) -> List[Card]:
        hand_cards = all_player_cards.copy()
        three_of_a_kind_cards = self._get_three_of_a_kind_cards(hand_cards)
        if len(three_of_a_kind_cards) == 0:
            return []
        for c in three_of_a_kind_cards:
            hand_cards.remove(c)
        first_pair = self._get_pair_cards(hand_cards)
        if len(first_pair) == 0:
            return []
        for c in first_pair:
            hand_cards.remove(c)
        second_pair = self._get_pair_cards(hand_cards)

        result = []
        if second_pair and second_pair[0] > first_pair[0]:
            result = three_of_a_kind_cards + second_pair
        else:
            result = three_of_a_kind_cards + first_pair
        return result

    def _get_four_of_a_kind_cards(self, all_player_cards: List[Card]) -> List[Card]:
        value_cards_map = defaultdict(list)
        for c in all_player_cards:
            value_cards_map[c.value].append(c)
            if len(value_cards_map[c.value]) == 4:
                return value_cards_map[c.value]
        return []

    def _get_straight_flush_cards(self, all_player_cards: List[Card]) -> List[Card]:

        flush_cards = self._get_flush_cards(all_player_cards, get_all_cards=True)
        if not flush_cards:
            return []

        straight_cards = self._get_straight_cards(flush_cards, get_all_cards=True)
        if not straight_cards:
            return []

        straight_flush_cards = flush_cards
        # check royal and smallest straight
        if straight_flush_cards[-1].value == 1 and straight_flush_cards[-2].value in (
            13,
            5,
        ):
            straight_flush_cards = straight_flush_cards[-5:]
        else:
            start_index = max(0, len(straight_flush_cards) - 1 - 5)
            # Slice the array from start_index to target_index
            straight_flush_cards = straight_flush_cards[start_index:-1]
        return straight_flush_cards

    def _get_royal_flush_cards(self, all_player_cards: List[Card]) -> List[Card]:
        straight_flush_cards = self._get_straight_flush_cards(all_player_cards)
        straight_flush_card_values = set([c.value for c in straight_flush_cards])

        ROYAL_FLUSH_VALUES = set([10, 11, 12, 13, 1])
        if ROYAL_FLUSH_VALUES <= straight_flush_card_values:
            return straight_flush_cards
        return []

    def evaluate_hand(
        self, all_player_cards: List[Card]
    ) -> tuple[HandResult, List[Card]]:
        if len(set(all_player_cards)) != 7:
            err_message = f"there must be 7 unique cards in hand for evaluation, found: {to_string(all_player_cards)}"
            logging.error(err_message)
            raise ValueError(err_message)
        hand_result, result_cards = HandResult.HIGH_CARD, []
        pair_cards = self._get_pair_cards(all_player_cards)
        if pair_cards:
            hand_result, result_cards = HandResult.PAIR, pair_cards

        two_pair_cards = self._get_two_pair_cards(all_player_cards)
        if two_pair_cards:
            hand_result, result_cards = (HandResult.TWO_PAIRS, two_pair_cards)

        three_of_a_kind_cards = self._get_three_of_a_kind_cards(all_player_cards)
        if three_of_a_kind_cards:
            hand_result, result_cards = (
                HandResult.THREE_OF_A_KIND,
                three_of_a_kind_cards,
            )

        straight_cards = self._get_straight_cards(all_player_cards)
        if straight_cards:
            hand_result, result_cards = (HandResult.STRAIGHT, straight_cards)

        flush_cards = self._get_flush_cards(all_player_cards)
        if flush_cards:
            hand_result, result_cards = HandResult.FLUSH, flush_cards

        full_house_cards = self._get_full_house_cards(all_player_cards)
        if full_house_cards:
            hand_result, result_cards = (HandResult.FULL_HOUSE, full_house_cards)

        four_of_a_kind_cards = self._get_four_of_a_kind_cards(all_player_cards)
        if four_of_a_kind_cards:
            hand_result, result_cards = (
                HandResult.FOUR_OF_A_KIND,
                four_of_a_kind_cards,
            )

        straight_flush_cards = self._get_straight_flush_cards(all_player_cards)
        if straight_flush_cards:
            hand_result, result_cards = (
                HandResult.STRAIGHT_FLUSH,
                straight_flush_cards,
            )

        royal_flush_cards = self._get_royal_flush_cards(all_player_cards)
        if royal_flush_cards:
            hand_result, result_cards = (HandResult.ROYAL_FLUSH, royal_flush_cards)

        if hand_result != HandResult.HIGH_CARD:
            return hand_result, result_cards

        sorted_cards = sorted(
            all_player_cards, key=lambda card: card.get_high_card_value()
        )
        return HandResult.HIGH_CARD, [sorted_cards[-1]]
