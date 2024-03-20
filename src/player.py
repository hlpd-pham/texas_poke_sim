import uuid
from typing import List

from card import Card
from game_evaluator import HandResult
from utils.strings import to_string


class Player:
    def __init__(
        self,
        id: str = "",
        cards: List[Card] = [],
        main_cards=[],
        kickers=[],
        hand_result=HandResult.HIGH_CARD,
    ):
        self.id = id if id is not None else uuid.uuid4()
        self.cards = cards
        self.hand_result: HandResult = hand_result
        self.main_cards: List[Card] = main_cards
        self.kickers: List[Card] = kickers

    def __str__(self):
        return (
            # f"Player(id:{self.id}, "
            f"Player("
            + f"{self.hand_result} - {self.hand_result.value}, "
            + f"cards:{to_string(self.cards)}, "
            + f"main_cards: {to_string(self.main_cards)}, "
            + f"kickers: {to_string(self.kickers)})"
        )

    def console_str(self):
        return (
            f"Player(id:{self.id}\n\t"
            + f"hand_result: {self.hand_result}\n\t"
            + f"cards:{to_string(self.cards)}\n\t"
            + f"main_cards: {to_string(self.main_cards)})\n\t"
            + f"kickers: {to_string(self.kickers)}"
        )
