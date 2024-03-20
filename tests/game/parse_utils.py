from card import Card, Suit
from player import Player

suit_map = {
    "heart": Suit.HEART,
    "diamond": Suit.DIAMOND,
    "spade": Suit.SPADE,
    "club": Suit.CLUB,
}


def parse_cards(cards_data_arr):
    return [
        Card(int(card_data["value"]), suit_map[card_data["suit"].lower()])
        for card_data in cards_data_arr
    ]


def parse_players(player_data_arr):
    res = []
    for player_data in player_data_arr:
        res.append(
            Player(
                id=player_data["ID"],
                cards=parse_cards(player_data["InitialDeal"]),
            )
        )
    return res
