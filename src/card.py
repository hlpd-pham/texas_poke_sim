import emoji
from aenum import Enum, NoAlias


class CardDealAmount(Enum):
    _settings_ = NoAlias

    PLAYER = 2
    BURN = 1
    FLOP = 3
    TURN = 1
    RIVER = 1


class Suit(Enum):
    """enum values are string values of the emojis for each suite"""

    HEART = ":heart_suit:"
    DIAMOND = ":diamond_suit:"
    CLUB = ":club_suit:"
    SPADE = ":spade_suit:"


class Card:

    def __init__(self, value: int = 1, suit: Suit = Suit.SPADE):
        self.value: int = value
        self.suit: Suit = suit

    def get_face_card_value(self):
        special_values = {
            1: "A",
            11: "J",
            12: "Q",
            13: "K",
        }
        return special_values.get(self.value, self.value)

    def get_card_value_suite(self):
        return self.value, self.suit

    def get_high_card_value(self):
        return 14 if self.value == 1 else self.value

    def __hash__(self):
        # Hash combination of name and age
        return hash((self.value, self.suit))

    def __eq__(self, other):
        if not isinstance(other, Card):
            # Don't attempt to compare against unrelated types
            return NotImplemented
        return self.suit == other.suit and self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, Card):
            # Don't attempt to compare against unrelated types
            return NotImplemented
        return self.value < other.value

    def __le__(self, other):
        return self < other or self == other

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __str__(self) -> str:
        return emoji.emojize(f"{self.get_face_card_value()}{self.suit.value} ")
