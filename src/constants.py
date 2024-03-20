import itertools

from card import Card, Suit

CARD_VALUES = range(1, 14)
ALL_CARDS = [
    Card(comb[0], comb[1])
    for comb in list(itertools.product(CARD_VALUES, list(Suit.__members__.values())))
]
