"""
Player(hand_result: HandResult.TWO_PAIRS, cards:['2♣️ ', 'J♠️ '], main_cards: ['2♣️ ', '2♥️ ', '4♠️ ', '4♦️ '], kickers: ['A♥️ '])
Player(hand_result: HandResult.TWO_PAIRS, cards:['J♦️ ', 'Q♦️ '], main_cards: ['4♠️ ', '4♦️ ', 'Q♦️ ', 'Q♠️ '], kickers: ['A♥️ '])
Player(hand_result: HandResult.TWO_PAIRS, cards:['A♦️ ', '8♣️ '], main_cards: ['A♦️ ', 'A♥️ ', '4♠️ ', '4♦️ '], kickers: ['Q♠️ '])
board
['A♥️ ', 'Q♠️ ', '4♠️ ', '2♥️ ', '4♦️ ']
"""

two_pair_1_winner = {
    "Title": "Higher 2 Pairs",
    "Players": [
        {
            "ID": "Player1",
            "InitialDeal": [
                {"value": "2", "suit": "club"},
                {"value": "11", "suit": "club"},
            ],
        },
        {
            "ID": "Player2",
            "InitialDeal": [
                {"value": "11", "suit": "diamond"},
                {"value": "12", "suit": "diamond"},
            ],
        },
        {
            "ID": "Player3",
            "InitialDeal": [
                {"value": "1", "suit": "diamond"},
                {"value": "8", "suit": "club"},
            ],
        },
    ],
    "Board": [
        {"value": "1", "suit": "heart"},
        {"value": "12", "suit": "spade"},
        {"value": "4", "suit": "spade"},
        {"value": "2", "suit": "heart"},
        {"value": "4", "suit": "diamond"},
    ],
    "Winners": ["Player3"],
}
