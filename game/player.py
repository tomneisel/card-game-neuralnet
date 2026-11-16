from game.card import Card

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand: list[Card] = []
        self.finished = False

    def add_cards(self, cards: list[Card]):
        self.hand.extend(cards)

    def play_cards(self, cards):
        for card in cards:
            if card not in self.hand:
                raise ValueError(f"Player does not have the card: {card}")

        for card in cards:
            self.hand.remove(card)

        if len(self.hand) == 0:
            self.finished = True

    def card_count(self):
        return len(self.hand)

    def __str__(self):
        return f"Player {self.player_id} ({self.card_count()} cards)"