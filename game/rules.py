from game.card import Card, Rank, Suit
from game.player import Player
from game.game_state import GameState
from game.action import Action

class Rules:

    def is_valid_combination(self, cards: list[Card]):
        if len(cards) == 0 or len(cards) > 4:
            return False

        if len(cards) == 1:
            return True

        first_rank = cards[0].rank
        for card in range(1, len(cards)):
            if cards[card].rank != first_rank:
                return False

        return True

    def can_beat(self, cards: list[Card], current_trick: list[Card]):
        if not current_trick:
            return True

        if len(cards) != len(current_trick):
            return False

        if cards[0].rank.value <= current_trick[0].rank.value:
            return False

        return True

    def get_legal_actions(self, game_state: GameState, player: Player):
        if player.finished:
            return []

        hand = player.hand

        possible_actions: list[Action] = []

        for card in hand:
            possible_actions.append(Action(cards=[card]))

        for card1 in range(len(hand)):
            combinations = [hand[card1]]
            for card2 in range(card1 + 1, len(hand)):
                if hand[card1].rank == hand[card2].rank:
                    combinations.append(hand[card2])
                    possible_actions.append(Action(cards=combinations.copy()))

        legal_actions: list[Action] = []

        for action in possible_actions:
            if self.can_beat(action.cards, game_state.current_trick):
                legal_actions.append(action)

        if game_state.current_trick:
            legal_actions.append(Action(is_pass=True))

        return legal_actions