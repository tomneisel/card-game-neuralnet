from game.card import Card, Suit, Rank
from game.player import Player
from game.game_state import GameState
from game.rules import Rules

player = Player(0)

card1 = Card(Rank.NINE, Suit.HEARTS)
card2 = Card(Rank.NINE, Suit.SPADES)
card3 = Card(Rank.SEVEN, Suit.DIAMONDS)
card4 = Card(Rank.KING, Suit.CLUBS)

player.add_cards([card1, card2, card3, card4])

game_state = GameState()
game_state.players = [player]
game_state.current_trick = []

rules = Rules()

legal_actions = rules.get_legal_actions(game_state, player)
print(len(legal_actions))

for action in legal_actions:
    if action.is_pass:
        print("Pass")
    else:
        print("Spiele:", action.cards)