from card import Card, Suit


def test_card_init():
    """init card and assert face value of regular cards"""
    card = Card(10, Suit.HEART)
    assert card is not None and card.suit == Suit.HEART and card.value == 10


def test_special_card():
    """init card and assert face value of special cards"""
    card = Card(1, Suit.HEART)
    assert card is not None and card.suit == Suit.HEART and card.value == 1

    card = Card(13, Suit.SPADE)
    assert card is not None and card.suit == Suit.SPADE and card.value == 13
