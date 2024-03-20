"""
start game for 5 players
board
['K♥️ ', 'K♣️ ', '9♣️ ', 'K♠️ ', '3♣️ ']

hand results
Player(HandResult.THREE_OF_A_KIND - 4, cards:['Q♣️ ', 'A♦️ '], main_cards: ['K♥️ ', 'K♣️ ', 'K♠️ '], kickers: ['Q♣️ ', 'A♦️ '])
Player(HandResult.FULL_HOUSE - 7, cards:['A♣️ ', '9♠️ '], main_cards: ['9♠️ ', '9♣️ ', 'K♥️ ', 'K♣️ ', 'K♠️ '], kickers: [])
Player(HandResult.THREE_OF_A_KIND - 4, cards:['5♣️ ', '8♥️ '], main_cards: ['K♥️ ', 'K♣️ ', 'K♠️ '], kickers: ['8♥️ ', '9♣️ '])
Player(HandResult.THREE_OF_A_KIND - 4, cards:['J♥️ ', '6♣️ '], main_cards: ['K♥️ ', 'K♣️ ', 'K♠️ '], kickers: ['9♣️ ', 'J♥️ '])
Player(HandResult.FULL_HOUSE - 7, cards:['10♥️ ', '10♦️ '], main_cards: ['10♥️ ', '10♦️ ', 'K♥️ ', 'K♣️ ', 'K♠️ '], kickers: [])
winners
Player(HandResult.FULL_HOUSE - 7, cards:['A♣️ ', '9♠️ '], main_cards: ['9♠️ ', '9♣️ ', 'K♥️ ', 'K♣️ '], kickers: [])
"""

full_house_higher_pair = {
    "Title": "Fullhouse Higher Pair",
    "Players": [
        {
            "ID": "Player1",
            "InitialDeal": [
                {"value": "1", "suit": "club"},
                {"value": "9", "suit": "spade"},
            ],
        },
        {
            "ID": "Player2",
            "InitialDeal": [
                {"value": "10", "suit": "heart"},
                {"value": "10", "suit": "diamond"},
            ],
        },
    ],
    "Board": [
        {"value": "13", "suit": "heart"},
        {"value": "13", "suit": "club"},
        {"value": "9", "suit": "club"},
        {"value": "13", "suit": "spade"},
        {"value": "3", "suit": "club"},
    ],
    "Winners": ["Player2"],
}
