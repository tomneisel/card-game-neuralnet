from game.card import Card, Rank, Suit
from game.deck import Deck
from game.player import Player
from game.rules import Rules
from game.game_state import GameState
from game.action import Action

class GameEngine:
    def __init__(self, rules: Rules, game_state: GameState):
        self.rules = rules
        self.game_state = game_state

    def start_game(self, deck_size=32, num_players=4):

        #resetting
        self.game_state.players = []
        self.game_state.current_trick = []
        self.game_state.last_player = None
        self.game_state.passed_players = []
        self.game_state.finished_players = []
        self.game_state.game_over = False
        self.game_state.final_ranking = []

        #creating deck
        deck = Deck(deck_size)
        deck.shuffle()

        #creating players
        for i in range(num_players):
            player = Player(i)
            self.game_state.players.append(player)

        #deal cards to players
        hands = deck.deal(num_players)

        for player, hand in zip(self.game_state.players, hands):
            player.hand = hand

        #find starting player
        starting_card = Card(Rank.SEVEN, Suit.DIAMONDS)
        for player in self.game_state.players:
            if starting_card in player.hand:
                self.game_state.current_player = player.player_id
                break

    def apply_action(self, player_id, action: Action):
        if self.game_state.game_over:
            raise ValueError("Game is already over!")

        if player_id != self.game_state.current_player:
            raise ValueError("It is not this player's turn!")

        player = self.game_state.players[player_id]

        legal_actions = self.rules.get_legal_actions(self.game_state, player)

        if action not in legal_actions:
            raise ValueError("This is not a legal move!")

        if action.is_pass:
            self.game_state.passed_players.append(player_id)

        else:
            player.play_cards(action.cards)

            self.game_state.current_trick = action.cards.copy()
            self.game_state.last_player = player_id
            self.game_state.passed_players = []

            if player.finished:
                self.game_state.finished_players.append(player_id)
   
        if self.check_trick_end():
            if self.game_state.last_player not in self.game_state.finished_players:
                self.game_state.current_player = self.game_state.last_player
            else:
                self.next_player()
            
            self.game_state.current_trick = []
            self.game_state.last_player = None
        else:
            self.next_player()

        if len(self.game_state.players) - len(self.game_state.finished_players) == 1:
            self.game_state.game_over = True
            self.game_state.final_ranking = self.game_state.finished_players.copy()
            self.game_state.final_ranking.append(self.game_state.current_player)

        
    def next_player(self):
        num_players = len(self.game_state.players)
        current = self.game_state.current_player

        for i in range(1, num_players + 1):
            next_id = (current + i) % num_players

            if next_id not in self.game_state.finished_players:
                self.game_state.current_player = next_id
                return

        self.game_state.game_over = True

    def check_trick_end(self):
        if not self.game_state.current_trick or self.game_state.last_player is None:
            return False

        if self.game_state.current_trick[0].rank.value == 14:
            return True

        active_opponents = [
            p.player_id
            for p in self.game_state.players
            if not p.finished and p.player_id != self.game_state.last_player
        ]

        if all(pid in self.game_state.passed_players for pid in active_opponents):
            return True

        return False