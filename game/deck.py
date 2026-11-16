import random

from game.card import Rank, Suit, Card

class Deck:
    def __init__(self, num_cards):
        self.num_cards = num_cards
        self.cards = []
        self.create_deck()

    def create_deck(self):
        self.cards = [
            Card(rank, suit) 
            for rank in Rank
            for suit in Suit
        ]
        self.cards = self.cards[-self.num_cards:]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_players):
        hands = [[] for _ in range(num_players)]

        for card in range(self.num_cards):
            hands[card % num_players].append(self.cards[card])

        self.cards = []

        return hands

    def reset(self):
        self.create_deck()